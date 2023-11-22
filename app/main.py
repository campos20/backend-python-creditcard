from fastapi import FastAPI, status, Depends
from config.dependencies_config import get_db
from schemas import CreditCardCreate

import service.credit_card_service as credit_card_service

from sqlalchemy.orm import Session


app = FastAPI()


@app.post("/api/v1/credit-cards", status_code=status.HTTP_201_CREATED)
def create_credit_card(
    credit_card_dto: CreditCardCreate, db: Session = Depends(get_db)
):
    return credit_card_service.create_credit_card(credit_card_dto, db)


@app.get("/api/v1/credit-cards")
def list_credit_cards(
    page: int = 1, page_size: int = 10, db: Session = Depends(get_db)
):
    return credit_card_service.list_credit_cards(page, page_size, db)


@app.get("/api/v1/credit-cards/{id}")
def detail_credit_card(credit_card_id: int, db: Session = Depends(get_db)):
    return credit_card_service.detail_credit_card(credit_card_id, db)
