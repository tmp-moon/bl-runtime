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

pipeline = None

class Framework(Enum):
    TRANSFORMERS = "transformers"
    DIFFUSERS = "diffusers"

class InferenceRequest(BaseModel):
    inputs: Union[str, List[str], object]
    parameters: Optional[Dict[str, Any]] = None


# Function to load the model asynchronously
async def load_model():
    global pipeline
    if not MODEL_ID or not FRAMEWORK:
        raise ValueError("MODEL_ID and FRAMEWORK must be defined in environment variables")
    
    if FRAMEWORK.lower() == "transformers":
        try:
            pipeline = transformers_pipeline(model=MODEL_ID, device_map=device)
            logger.info(f"Model {MODEL_ID} loaded successfully using {FRAMEWORK} framework")
        except Exception as e:
            logger.error(f"Error loading transformers model: {e}")
            raise
    elif FRAMEWORK.lower() == "diffusers":
        try:
            pipeline = diffusers_pipeline.from_pretrained(MODEL_ID, device_map=device)
            logger.info(f"Model {MODEL_ID} loaded successfully using {FRAMEWORK} framework")
        except Exception as e:
            logger.error(f"Error loading diffusers model: {e}")
            raise
    else:
        raise ValueError(f"Invalid framework: {FRAMEWORK}")

# Define a lifespan context manager
async def lifespan(app: FastAPI):
    logger.info(f"Starting to load model {MODEL_ID} with framework {FRAMEWORK}")
    background_tasks = BackgroundTasks()
    background_tasks.add_task(load_model)
    await background_tasks()
    yield
    # Any cleanup code can go here

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
FRAMEWORK = args.framework or os.getenv("FRAMEWORK")

# Ensure the lifespan function is defined before this line
app = FastAPI(title="api", lifespan=lifespan)

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
    uvicorn.run(app, host="0.0.0.0", port=4321)
