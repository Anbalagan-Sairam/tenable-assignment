import joblib
import os
import time
import json
from fastapi import FastAPI, Request
from pydantic import BaseModel

# ----- Model Loading -----
MODEL_PATH = "model.pkl"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"{MODEL_PATH} not found. Run train_model.py first.")

model = joblib.load(MODEL_PATH)  # Load model once at startup

# ----- FastAPI App -----
app = FastAPI(title="Titanic Survival Predictor")

# ----- Input Schema -----
class PassengerFeatures(BaseModel):
    pclass: int
    age: float
    sibsp: int
    fare: float

# ----- Observability Middleware -----
request_count = 0  # global counter

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
        "status_code": response.status_code
    }
    print(json.dumps(log))  # logs appear in terminal in JSON format
    return response

# ----- Prediction Endpoint -----
@app.post("/predict")
def predict(features: PassengerFeatures):
    X = [[features.pclass, features.age, features.sibsp, features.fare]]
    prob = model.predict_proba(X)[0][1]  # probability of survival (class 1)
    return {"survival_probability": prob}