from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"


class WalletCreate(BaseModel):
    name: str
    balance: float
    initial_balance: float
    currency: str


class WalletResponse(BaseModel):
    id: int
    name: str
    balance: float
    initial_balance: float
    currency: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True