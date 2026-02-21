from pydantic import BaseModel
from datetime import datetime

class CategoryCreate(BaseModel):
    name: str
    type: str  # 'income' or 'expense'

class CategoryResponse(BaseModel):
    id: int
    user_id: int
    name: str
    type: str
    created_at: datetime

    class Config:
        model_config = {
            "from_attributes": True
        }
        
