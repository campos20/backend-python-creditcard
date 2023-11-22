from fastapi.testclient import TestClient
from fastapi import status

from main import app

client = TestClient(app)


def test_create_credit_card():
    data = {
        "card_number": "string",
        "card_holder": "string",
        "expiration_date": "string",
        "cvv": "string",
    }
    response = client.post(
        "/api/v1/credit-card",
        json=data,
    )
    assert response.status_code == status.HTTP_201_CREATED
