from pydantic import BaseModel, validator
from datetime import datetime

from creditcard import CreditCard as ValidateCreditCard

from config.constants_config import EXPIRATION_DT_FORMAT


class CreditCardCreate(BaseModel):
    card_number: str
    card_holder: str
    expiration_date: str
    cvv: str

    def is_valid(self):
        cc = ValidateCreditCard(self.card_number)
        return cc.is_valid()

    @validator("expiration_date")
    def parse_expiration_date(cls, v):
        """Validates expiration_date as mm/yyyy"""

        return datetime.strptime(v, EXPIRATION_DT_FORMAT).strftime(EXPIRATION_DT_FORMAT)

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
        },
    }


class CreditCardDto(CreditCardCreate, BaseModel):
    id: int
