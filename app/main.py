from fastapi import Depends, FastAPI, status
from config.database import Base, SessionLocal, engine

from dto.credit_card_dto import CreditCardDto
from model.credit_card import CreditCard
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/v1/credit-card", status_code=status.HTTP_201_CREATED)
def create_credit_card(credit_card_dto: CreditCardDto, db: Session = Depends(get_db)):
    db_credit_card = CreditCard()
    db_credit_card.card_holder = credit_card_dto.card_holder
    db_credit_card.card_number = credit_card_dto.card_number
    db_credit_card.expiration_date = credit_card_dto.expiration_date
    db_credit_card.cvv = credit_card_dto.cvv

    db.add(db_credit_card)
    db.commit()
    db.refresh(db_credit_card)
    return credit_card_dto
