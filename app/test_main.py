from fastapi.testclient import TestClient
from fastapi import status

from parameterized import parameterized

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
        "/api/v1/credit-cards",
        json=json,
    )
    assert response.status_code == status.HTTP_201_CREATED


@parameterized.expand(
    [
        (None, "card_holder", "expiration_date", "cvv"),  # Missing card number
        ("card_number", None, "expiration_date", "cvv"),  # Missing card holder
        ("card_number", "card_holder", None, "cvv"),  # Missing expirationr
        ("card_number", "card_holder", "expiration_date", None),  # Missing cvv
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
        "/api/v1/credit-cards",
        json=json,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_list_credit_card():
    response = client.get("/api/v1/credit-cards")
    assert response.status_code == status.HTTP_200_OK


@parameterized.expand(
    [
        (1, status.HTTP_200_OK),
        (-1, status.HTTP_404_NOT_FOUND),  # Non existing,
        ("non_numeric", status.HTTP_422_UNPROCESSABLE_ENTITY),  # String instead
    ]
)
def test_detail_credit_card(id, status_code):
    response = client.get(f"/api/v1/credit-cards/{id}")
    assert response.status_code == status_code
