FROM python:3.12

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install diffusers transformers fastapi uvicorn accelerate>=0.26.0

COPY main.py main.py

ENTRYPOINT ["python", "main.py"]