from fastapi import HTTPException, status
from helper.page_helper import create_page

from model.credit_card import CreditCard
from sqlalchemy.orm import Session

from schemas import CreditCardCreate, CreditCardDto


def create_credit_card(credit_card_create: CreditCardCreate, db: Session):
    if not credit_card_create.is_valid():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Credit card number '{credit_card_create.card_number}' is not valid",
        )

    db_credit_card = CreditCard(**credit_card_create.model_dump())

    db.add(db_credit_card)
    db.commit()
    db.refresh(db_credit_card)

    return CreditCardDto(**credit_card_create.model_dump(), id=db_credit_card.id)


def list_credit_cards(page: int, page_size: int, db: Session):
    offset = (page - 1) * page_size
    total_count = db.query(CreditCard.id).count()

    items = db.query(CreditCard).offset(offset).limit(page_size).all()

    # Pydantically parse objects to avoid leaking details of the model
    content = [CreditCardDto(**item.__dict__) for item in items]

    return create_page(content, page, page_size, total_count)


def detail_credit_card(credit_card_id: int, db: Session):
    db_credit_card = (
        db.query(CreditCard).filter(CreditCard.id == credit_card_id).first()
    )

    if db_credit_card is None:
        raise HTTPException(status_code=404, detail="Credit card not found")
    return db_credit_card
