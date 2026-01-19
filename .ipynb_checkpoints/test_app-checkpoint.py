import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the FastAPI app
from app import app

client = TestClient(app)

# Unit test
def test_predict_with_mocked_model():
    # Create a fake model that always returns 0.5 probability using unittest library
    fake_model = MagicMock()
    fake_model.predict_proba.return_value = [[0.5, 0.5]]

    # Patch the 'model' in app.py to use the fake model
    with patch("app.model", fake_model):
        response = client.post(
            "/predict",
            json={"pclass": 1, "age": 28, "sibsp": 0, "fare": 10}
        )
        assert response.status_code == 200
        data = response.json()
        # Check that the API returns a survival_probability key
        assert "survival_probability" in data
        # Check that the mocked model returned 0.5
        assert data["survival_probability"] == 0.5
        print("STATUS:", response.status_code)
        print("BODY:", response.json())

# Input test validation
def test_predict_input_validation():
    response = client.post(
        "/predict",
        json={"pclass": "one", "age": "twenty", "sibsp": 0, "fare": 10}
    )
    assert response.status_code == 422
    print("STATUS:", response.status_code)
    print("BODY:", response.json())