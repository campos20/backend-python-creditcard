from datetime import date
from fastapi.testclient import TestClient
from fastapi import status

from parameterized import parameterized
from config.constants_config import EXPIRATION_DT_FORMAT

from main import app

from dateutil.relativedelta import relativedelta

client = TestClient(app)

today = date.today()

VALID_CREDIT_CARD = {
    "card_holder": "John Doe",
    "card_number": "4539578763621486",
    "cvv": "012",
    "expiration_date": f"{today.month}/{today.year+1}",
}


def test_create_credit_card():
    response = client.post(
        "/api/v1/credit-cards",
        json=VALID_CREDIT_CARD,
    )
    assert response.status_code == status.HTTP_201_CREATED


@parameterized.expand(
    [
        (
            "expiration_date",  # Expired card
            (date.today() - relativedelta(months=1)).strftime(EXPIRATION_DT_FORMAT),
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "card_number",  # Invalid card number
            "0123456789",
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "card_holder",  # Small size card holder
            "A",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            "cvv",  # Big size cvv
            "12345",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            "cvv",  # Small size cvv
            "12",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            "cvv",  # Non numeric cvv
            "abc",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ]
)
def test_create_credit_card_fail(field_name, new_value, status_code):
    json = VALID_CREDIT_CARD | {field_name: new_value}
    response = client.post(
        "/api/v1/credit-cards",
        json=json,
    )
    assert response.status_code == status_code


@parameterized.expand(
    [
        ("card_number", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("card_holder", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("expiration_date", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("cvv", status.HTTP_201_CREATED),  # CVV is optional
    ]
)
def test_create_credit_card_missing_property(field_name, status_code):
    # The | operator merges the dict, making one of the fields as None
    json = VALID_CREDIT_CARD | {field_name: None}

    response = client.post(
        "/api/v1/credit-cards",
        json=json,
    )
    assert response.status_code == status_code


@parameterized.expand(
    [
        (None, None, status.HTTP_200_OK),  # page and size are optional
        (1, 10, status.HTTP_200_OK),  # valid page size
        (0, 10, status.HTTP_422_UNPROCESSABLE_ENTITY),  # page should be >= 1
        (1, 101, status.HTTP_422_UNPROCESSABLE_ENTITY),  # page_size should be <= 100
    ]
)
def test_list_credit_card(page, page_size, stauts_code):
    params = {}
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size

    response = client.get("/api/v1/credit-cards", params=params)
    assert response.status_code == stauts_code


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
