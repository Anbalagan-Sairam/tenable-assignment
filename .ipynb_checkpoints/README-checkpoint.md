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
## Part 2: Observability & Metrics

Added Observability middleware that the logs the number of request made with total time taken

## Part 3: Testing

For this step, unit tests were written using pytest to validate the API logic without loading the heavy ML model artifact. The model is mocked using Python’s `unittest.mock` library so the tests only validate the API response structure, input validation, and overall request handling.

Run the following command to perform unit testing
```bash
pytest -s
```

Output:
```bash
test_app.py {"request_number": 1, "path": "/predict", "method": "POST", "latency_sec": 0.0021, "status_code": 200}
STATUS: 200
BODY: {'survival_probability': 0.5}
.{"request_number": 2, "path": "/predict", "method": "POST", "latency_sec": 0.0009, "status_code": 422}
STATUS: 422
BODY: {'detail': [{'type': 'int_parsing', 'loc': ['body', 'pclass'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'input': 'one'}, {'type': 'float_parsing', 'loc': ['body', 'age'], 'msg': 'Input should be a valid number, unable to parse string as a number', 'input': 'twenty'}]}
```

## Part 4: Containerization
The FastAPI service is containerized using Docker to ensure consistency across different environments. A lightweight Python base image is used and only the required dependencies are included to keep the image minimal and secure. The container runs the application using Uvicorn and exposes the API on port 8000, making it easy to deploy and run in both local and cloud environments.

The following command is used to containerize in AWS Sagemaker:
```bash
sm-docker build .
```

Once run, I am able to obtain a docker image which I can view from ECR Repo.

```bash
972729655482.dkr.ecr.us-east-1.amazonaws.com/sagemaker-studio-d-fi0qlan4ewgx:default-20260115T160644
```

## Part 5: CI/CD & Deployment

A basic CI pipeline is added using GitHub Actions to ensure code quality and reliability on every push and to check guardrails. The pipeline is present in tenable_assignment/.github/workflows/ci.yml. The code consists of five steps to setup repo code, python environment, install requirements.txt, run static code linting and execute all unit test using pytest.
The pipeline runs for every push to code in github. values.yml contains the deployment settings for kubernetes.
