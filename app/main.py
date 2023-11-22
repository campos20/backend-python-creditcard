from fastapi import Depends, FastAPI, status
from config.database import Base, SessionLocal, engine

from model.credit_card import CreditCard
from sqlalchemy.orm import Session

from schemas import CreditCardCreate, CreditCardDto

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/v1/credit-cards", status_code=status.HTTP_201_CREATED)
def create_credit_card(
    credit_card_dto: CreditCardCreate, db: Session = Depends(get_db)
):
    db_credit_card = CreditCard(**credit_card_dto.model_dump())

    db.add(db_credit_card)
    db.commit()
    db.refresh(db_credit_card)

    return CreditCardDto(**credit_card_dto.model_dump(), id=db_credit_card.id)


@app.get("/api/v1/credit-cards")
def list_credit_cards(
    page: int = 0, page_size: int = 10, db: Session = Depends(get_db)
):
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
