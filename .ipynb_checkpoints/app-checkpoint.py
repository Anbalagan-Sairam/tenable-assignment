import joblib
import os
import time
import json
from fastapi import FastAPI, Request
from pydantic import BaseModel


MODEL_PATH = "model.pkl"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"{MODEL_PATH} not found")

model = joblib.load(MODEL_PATH)


app = FastAPI(title="Titanic Survival Predictor")


class PassengerFeatures(BaseModel):
    pclass: int
    age: float
    sibsp: int
    fare: float


request_count = 0


@app.middleware("http")
async def log_requests(request: Request, call_next):
    global request_count
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    request_count += 1

    log = {
        "request_number": request_count,
        "path": request.url.path,
        "method": request.method,
        "latency_sec": round(process_time, 4),
        "status_code": response.status_code,
    }

    print(json.dumps(log))
    return response


@app.post("/predict")
def predict(features: PassengerFeatures):
    X = [[features.pclass, features.age, features.sibsp, features.fare]]

    prob = model.predict_proba(X)[0][1]

    return {"survival_probability": prob}