from pydantic import BaseModel


class CreditCardDto(BaseModel):
    card_number: str
    card_holder: str
    expiration_date: str
    cvv: str
