from typing import Annotated
from fastapi import FastAPI, HTTPException, Query, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.dependencies_config import get_db
from schemas import CreditCardCreate
from security import decode_jwt_token, generate_jwt_for

import service.credit_card_service as credit_card_service

from sqlalchemy.orm import Session

from config.database_config import Base, engine


Base.metadata.create_all(bind=engine)


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return decode_jwt_token(token)


@app.post("/api/v1/credit-cards", status_code=status.HTTP_201_CREATED)
def create_credit_card(
    credit_card_create: CreditCardCreate,
    _current_user: Annotated[dict, Depends(get_current_user)],  # Only for authorization
    db: Session = Depends(get_db),
):
    return credit_card_service.create_credit_card(credit_card_create, db)


@app.get("/api/v1/credit-cards")
def list_credit_cards(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
    db: Session = Depends(get_db),
):
    return credit_card_service.list_credit_cards(page, page_size, db)


@app.get("/api/v1/credit-cards/{credit_card_id}")
def detail_credit_card(credit_card_id: int, db: Session = Depends(get_db)):
    return credit_card_service.detail_credit_card(credit_card_id, db)


@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = form_data.username
    password = form_data.password
    if not username or username != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials (for this exercise, user should equals password)",
        )
    token = generate_jwt_for(username)

    return {"access_token": token, "token_type": "bearer"}
