# AI Engineer: Technical Assignment


## Goal
The goal for this assignment is to operationalise a raw scikit-learn model into a production-ready microservice with strong engineering design, observability, testing, containerisation and CI/CD.

## Part 0: The Setup
In order to tackle the assignment, I am choosing AWS as my cloud provider and using its services such as Sagemaker unified studio, S3, ECS etc. The file is executed to generate `model.pkl` artifact.

```bash
python train_model.py
```

## Part 1: API Implementation
Created app.py which exposes a `POST /predict` endpoint that accepts Titanic passenger features (`pclass`, `age`, `sibsp`, `fare`) and returns a survival probability.
