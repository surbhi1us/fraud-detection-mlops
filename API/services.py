
import sys
import joblib
import pandas as pd
import numpy as np

import Src.model as model_module

from Src.model import (
    FraudPipeline,
    FeatureEngineering,
    LogTransformer,
    Preprocessing,
)

# Make custom classes available under the module name
# stored in the original pickle.
sys.modules["__main__"] = model_module

MODEL_PATH = "/app/Notebooks/fraud_pipeline_deployed.pkl"
model = joblib.load(MODEL_PATH)


def predict_fraud(data: dict):
    df = pd.DataFrame([data])
    df = df.where(pd.notnull(df), np.nan)
    preds = model.predict(df)
    return int(preds[0])
