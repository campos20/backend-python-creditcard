from fastapi import FastAPI, status

from dto.credit_card_dto import CreditCardDto

app = FastAPI()


@app.post("/api/v1/credit-card", status_code=status.HTTP_201_CREATED)
def create_credit_card(credit_card_dto: CreditCardDto):
    return credit_card_dto
