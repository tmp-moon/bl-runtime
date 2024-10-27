FROM python:3.12

RUN pip install diffusers transformers fastapi uvicorn

COPY main.py main.py

ENTRYPOINT ["python", "main.py"]