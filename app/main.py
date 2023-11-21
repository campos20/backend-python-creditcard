from fastapi import FastAPI

app = FastAPI()


@app.post("/api/v1/credit-card")
def create_credit_card():
    return {}
