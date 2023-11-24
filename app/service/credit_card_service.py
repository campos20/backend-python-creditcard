from datetime import datetime, date
from fastapi import HTTPException, status
from config.constants_config import EXPIRATION_DT_FORMAT
from helper.hash_helper import hash_all_but_last_n_chars
from helper.page_helper import create_page

from model.credit_card import CreditCard
from sqlalchemy.orm import Session

from schemas import CreditCardCreate, CreditCardDto

from dateutil.relativedelta import relativedelta


def create_credit_card(credit_card_create: CreditCardCreate, db: Session):
    if not credit_card_create.is_valid():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Credit card number '{credit_card_create.card_number}' is not valid",
        )

    # Expiration date as the last day of month
    expiration_date = (
        datetime.strptime(credit_card_create.expiration_date, EXPIRATION_DT_FORMAT)
        + relativedelta(months=1)
        - relativedelta(days=1)
    ).date()

    if expiration_date < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Credit card is expired"
        )

    db_credit_card = CreditCard(**credit_card_create.model_dump())
    db_credit_card.expiration_date = expiration_date
    db_credit_card.brand = credit_card_create.get_brand()
    db_credit_card.card_number = hash_all_but_last_n_chars(
        credit_card_create.card_number, 4
    )

    db.add(db_credit_card)
    db.commit()
    db.refresh(db_credit_card)

    return _credit_card_to_dto(db_credit_card)


def list_credit_cards(page: int, page_size: int, db: Session):
    offset = (page - 1) * page_size
    total_count = db.query(CreditCard.id).count()

    items = db.query(CreditCard).offset(offset).limit(page_size).all()

    content = [_credit_card_to_dto(item) for item in items]

    return create_page(content, page, page_size, total_count)


def detail_credit_card(credit_card_id: int, db: Session):
    db_credit_card = (
        db.query(CreditCard).filter(CreditCard.id == credit_card_id).first()
    )

    if db_credit_card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Credit card not found"
        )
    return _credit_card_to_dto(db_credit_card)


def _credit_card_to_dto(item: CreditCard):
    # Pydantically parse objects to avoid leaking details of the model

    return CreditCardDto(
        **item.__dict__
        | {"expiration_date": item.expiration_date.strftime(EXPIRATION_DT_FORMAT)}
    )
