from fastapi import FastAPI
from pydantic import BaseModel

import joblib
import numpy as np
import tensorflow as tf

import os

print(os.getcwd())
print(os.listdir())
print(os.listdir("model"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(BASE_DIR, "..", "model")

preprocessor = joblib.load(os.path.join(MODEL_DIR, "preprocessor.pkl"))
xgb_model = joblib.load(os.path.join(MODEL_DIR, "xgb_model.pkl"))
ann_model = tf.keras.models.load_model(os.path.join(MODEL_DIR, "ann_model.h5"))

app = FastAPI(
    title="Sepsis Risk Prediction API",
    description="API for predicting sepsis risk using Ensemble Model (XGBoost + ANN)",
    version="1.0"
)


class PatientData(BaseModel):

    heart_rate: float
    respiratory_rate: float
    temperature: float
    wbc_count: float
    lactate_level: float
    age: int
    num_comorbidities: int


@app.get("/")
def home():
    return {"message": "Sepsis Risk Prediction API is running"}


@app.post("/predict")
def predict(data: PatientData):

    # Convert input to numpy array
    input_data = np.array([[
        data.heart_rate,
        data.respiratory_rate,
        data.temperature,
        data.wbc_count,
        data.lactate_level,
        data.age,
        data.num_comorbidities
    ]])

    # Preprocess data
    processed = preprocessor.transform(input_data)

    # Predict using XGBoost
    xgb_prob = xgb_model.predict_proba(input_data)[0][1]

    # Predict using ANN
    ann_prob = ann_model.predict(processed)[0][0]

    # Ensemble prediction
    final_prob = (0.6 * xgb_prob) + (0.4 * ann_prob)

    # Convert probability to class
    prediction = int(final_prob > 0.5)

    return {
        "sepsis_risk_prediction": prediction,
        "risk_probability": float(final_prob)
    }