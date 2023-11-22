from fastapi.testclient import TestClient
from fastapi import status

from parameterized import parameterized, parameterized_class

from main import app

client = TestClient(app)


def test_create_credit_card():
    json = {
        "card_number": "string",
        "card_holder": "string",
        "expiration_date": "string",
        "cvv": "string",
    }
    response = client.post(
        "/api/v1/credit-card",
        json=json,
    )
    assert response.status_code == status.HTTP_201_CREATED


@parameterized.expand(
    [
        (None, "card_holder", "expiration_date", "cvv"),
        ("card_number", None, "expiration_date", "cvv"),
        ("card_number", "card_holder", None, "cvv"),
        ("card_number", "card_holder", "expiration_date", None),
    ]
)
def test_create_credit_card_missing_property(
    card_number, card_holder, expiration_date, cvv
):
    json = {
        "card_number": card_number,
        "card_holder": card_holder,
        "expiration_date": expiration_date,
        "cvv": cvv,
    }
    response = client.post(
        "/api/v1/credit-card",
        json=json,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
