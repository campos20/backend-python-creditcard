from pydantic import BaseModel


class CreditCardCreate(BaseModel):
    card_number: str
    card_holder: str
    expiration_date: str
    cvv: str


class CreditCardDto(CreditCardCreate, BaseModel):
    id: int
