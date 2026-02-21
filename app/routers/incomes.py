from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.models.incomes import Income
from app.utils.database import AsyncSession
from app.schemas.incomes import IncomeCreate, IncomeResponse
from app.utils.database import get_db
from app.utils.dependencies import get_current_user
from app.models.users import User

router = APIRouter(
    prefix="/incomes",
    tags=["incomes"]
)

@router.post("/create", response_model=IncomeResponse)
async def create_income(
    income: IncomeCreate,
    current_user: User = Depends(get_current_user),  
    db: AsyncSession = Depends(get_db)
):
    new_income = Income(
        amount=income.amount,
        description=income.description,
        date=income.date,
        user_id=current_user.id,
        wallet_id=income.wallet_id,
        category_id=income.category_id
    )

    db.add(new_income)
    await db.commit()
    await db.refresh(new_income)

    return new_income