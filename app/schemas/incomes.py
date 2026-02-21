from pydantic import BaseModel
from datetime import datetime


class IncomeCreate(BaseModel):
    amount: float
    description: str
    date: datetime
    user_id: int
    wallet_id: int
    category_id: int

class IncomeResponse(BaseModel):
    id: int
    amount: float
    description: str
    date: datetime
    user_id: int
    wallet_id: int
    category_id: int

    class Config:
        from_attributes = True


