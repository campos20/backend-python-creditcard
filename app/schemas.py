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

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "card_number": "4539578763621486",
                    "card_holder": "John Doe",
                    "expiration_date": "02/2026",
                    "cvv": "012",
                }
            ]
        }
    }


class CreditCardDto(CreditCardCreate, BaseModel):
    id: int
