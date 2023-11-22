from fastapi import HTTPException

from model.credit_card import CreditCard
from sqlalchemy.orm import Session

from schemas import CreditCardCreate, CreditCardDto


def create_credit_card(credit_card_dto: CreditCardCreate, db: Session):
    db_credit_card = CreditCard(**credit_card_dto.model_dump())

    db.add(db_credit_card)
    db.commit()
    db.refresh(db_credit_card)

    return CreditCardDto(**credit_card_dto.model_dump(), id=db_credit_card.id)


def list_credit_cards(page: int, page_size: int, db: Session):
    offset = (page - 1) * page_size
    total_count = db.query(CreditCard.id).count()
    total_pages = (total_count + page_size - 1) // page_size

    items = db.query(CreditCard).offset(offset).limit(page_size).all()

    # Pydantically parse objects to avoid leaking details of the model
    content = [CreditCardDto(**item.__dict__) for item in items]

    return {
        "content": content,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "total": total_count,
    }


def detail_credit_card(credit_card_id: int, db: Session):
    db_credit_card = (
        db.query(CreditCard).filter(CreditCard.id == credit_card_id).first()
    )

    if db_credit_card is None:
        raise HTTPException(status_code=404, detail="Credit card not found")
    return db_credit_card
