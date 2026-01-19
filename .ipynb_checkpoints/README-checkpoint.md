# AI Engineer: Technical Assignment


## Goal
The goal for this assignment is to operationalise a raw scikit-learn model into a production-ready microservice with strong engineering design, observability, testing, containerisation and CI/CD.

## Part 0: The Setup
In order to tackle the assignment, I am choosing AWS as my cloud provider and using its services such as Sagemaker unified studio, S3, ECS etc. The file is executed to generate `model.pkl` artifact.

```bash
python train_model.py
```

## Part 1: API Implementation
Created app.py which exposes a `POST /predict` endpoint that accepts Titanic passenger features (`pclass`, `age`, `sibsp`, `fare`) and returns a survival probability. joblib is used to load the model efficiently so that inference is fast and efficient.

We start the FastAPI server from app.py and expose the API on port 8000 using the following command:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Sending POST request in order to get prediction

```bash
curl -X POST "http://localhost:8000/predict"   -H "Content-Type: application/json"   -d '{"pclass": 1, "age": 28, "sibsp": 0, "fare": 10}'  | jq
```

The following response is obtained:

```bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    91  100    43  100    48   3362   3752 --:--:-- --:--:-- --:--:--  7583
{
  "survival_probability": 0.6610708874611355
}
```