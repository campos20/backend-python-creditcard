from pydantic import BaseModel

from creditcard import CreditCard as ValidateCreditCard


class CreditCardCreate(BaseModel):
    card_number: str
    card_holder: str
    expiration_date: str
    cvv: str

    def is_valid(self):
        cc = ValidateCreditCard(self.card_number)
        return cc.is_valid()


class CreditCardDto(CreditCardCreate, BaseModel):
    id: int
