from typing import Dict, Union, Any, Optional, List
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi import BackgroundTasks
from pydantic import BaseModel
from transformers import pipeline as transformers_pipeline
from diffusers import DiffusionPipeline as diffusers_pipeline
from enum import Enum
import torch
import uvicorn
import logging
import sys
import os
import argparse
import requests

pipeline = None

class Framework(Enum):
    TRANSFORMERS = "transformers"
    DIFFUSERS = "diffusers"

class InferenceRequest(BaseModel):
    inputs: Union[str, List[str], object]
    parameters: Optional[Dict[str, Any]] = None


# Function to get model metadata from Hugging Face
def get_model_metadata(model_id: str) -> Dict[str, Any]:
    url = f"https://huggingface.co/api/models/{model_id}"
    headers = {}
    if HF_API_TOKEN:
        headers["Authorization"] = f"Bearer {HF_API_TOKEN}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch model metadata for {model_id}")
    return response.json()

# Function to load the model synchronously
def load_model():
    global pipeline
    if not MODEL_ID:
        raise ValueError("MODEL_ID must be defined in environment variables or arguments")
    
    logger.info("Starting model loading process...")

    # Fetch model metadata
    metadata = get_model_metadata(MODEL_ID)
    logger.info("Fetched model metadata (20%)")
    tags = metadata.get("tags", [])
    
    # Determine framework from tags
    if "transformers" in tags:
        framework = "transformers"
    elif "diffusers" in tags:
        framework = "diffusers"
    else:
        raise ValueError(f"Framework not found in model tags for {MODEL_ID}")

    logger.info(f"Determined framework: {framework} (40%)")

    if framework == "transformers":
        try:
            pipeline = transformers_pipeline(model=MODEL_ID, device_map=device, use_auth_token=HF_API_TOKEN)
            logger.info(f"Model {MODEL_ID} loaded successfully using {framework} framework (100%)")
        except Exception as e:
            logger.error(f"Error loading transformers model: {e}")
            raise
    elif framework == "diffusers":
        try:
            pipeline = diffusers_pipeline.from_pretrained(MODEL_ID, device_map=device, use_auth_token=HF_API_TOKEN)
            logger.info(f"Model {MODEL_ID} loaded successfully using {framework} framework (100%)")
        except Exception as e:
            logger.error(f"Error loading diffusers model: {e}")
            raise
    else:
        raise ValueError(f"Invalid framework: {framework}")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

device = "cuda" if torch.cuda.is_available() else "cpu"

# Add this function to parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the API server with specified model and framework.")
    parser.add_argument("--model-id", type=str, help="The model id to use")
    parser.add_argument("--framework", type=str, choices=["transformers", "diffusers"], help="The framework to use")
    return parser.parse_args()

# Modify the code near the environment variable retrieval
args = parse_arguments()

# Retrieving model and framework from arguments or environment variables
MODEL_ID = args.model_id or os.getenv("MODEL_ID")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

app = FastAPI(title="api")

@app.get("/health")
def health():
    return JSONResponse(status_code=200, content={"status": "ok"})


@app.post("/")
def infer(request: InferenceRequest):
    logger.info("Received request", extra={"request": request})
    if request.parameters is None:
        request.parameters = {}
    if isinstance(request.inputs, str):
        resp = pipeline(request.inputs, **request.parameters)
    elif isinstance(request.inputs, list):
        resp = pipeline(*request.inputs, **request.parameters)
    else:
        resp = pipeline(**request.inputs, **request.parameters)
    return JSONResponse(status_code=200, content=resp)


if __name__ == "__main__":
    # Load the model before starting the server
    load_model()
    uvicorn.run(app, host="0.0.0.0", port=4321)
