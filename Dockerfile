
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY API/ ./API/
COPY Src/ ./Src/
COPY Notebooks/mlruns/ ./Notebooks/mlruns/

COPY Notebooks/fraud_pipeline_deployed.pkl ./Notebooks/fraud_pipeline_deployed.pkl
ENV MLFLOW_TRACKING_URI=file:///app/Notebooks/mlruns
ENV MLFLOW_ALLOW_FILE_STORE=true

EXPOSE 8000

CMD ["uvicorn", "API.main:app", "--host", "0.0.0.0", "--port", "8000"]
