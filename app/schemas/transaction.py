from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    amount: float
    description: str | None = None
    date: datetime
    type: str  # "income" или "expense"
    wallet_id: int | None = None
    category_id: int | None = None


class TransactionResponse(BaseModel):
    id: int
    amount: float
    description: str | None
    date: datetime
    type: str
    user_id: int
    wallet_id: int | None
    category_id: int | None

    class Config:
        from_attributes = True
