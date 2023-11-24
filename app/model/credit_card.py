from sqlalchemy import Column, Date, Integer, String

from config.database_config import Base


class CreditCard(Base):
    __tablename__ = "credit_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, index=True)
    card_holder = Column(String)
    expiration_date = Column(Date)
    cvv = Column(String)
    brand = Column(String)
