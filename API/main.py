
from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram
from API.schemas import FraudRequest, FraudResponse
from API.services import predict_fraud
from prometheus_fastapi_instrumentator import Instrumentator
import time

app = FastAPI(
    title="Fraud Detection API",
    description="Predict fraudulent transactions using a machine learning model",
    version="1.0.0"
)

# Standard HTTP request metrics
Instrumentator().instrument(app).expose(app)

# Custom fraud prediction metrics
PREDICTION_COUNT = Counter(
    "fraud_predictions_total",
    "Total number of fraud predictions",
    ["result"]
)

PREDICTION_ERRORS = Counter(
    "fraud_prediction_errors_total",
    "Total number of failed fraud predictions"
)

PREDICTION_LATENCY = Histogram(
    "fraud_prediction_latency_seconds",
    "Time taken to make a fraud prediction"
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict", response_model=FraudResponse)
def predict(request: FraudRequest):
    start_time = time.perf_counter()

    try:
        prediction = predict_fraud(request.dict())

        # Record the predicted class
        PREDICTION_COUNT.labels(result=str(prediction)).inc()

        return FraudResponse(prediction=prediction)

    except Exception:
        PREDICTION_ERRORS.inc()
        raise

    finally:
        PREDICTION_LATENCY.observe(
            time.perf_counter() - start_time
        )
