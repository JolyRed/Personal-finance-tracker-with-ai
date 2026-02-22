from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.models.transaction import Transaction
from app.utils.database import AsyncSession
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.utils.database import get_db
from app.utils.dependencies import get_current_user
from app.models.users import User

router = APIRouter(
    prefix="/incomes",
    tags=["incomes"]
)

@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_transaction = Transaction(
        amount=transaction.amount,
        description=transaction.description,
        date=transaction.date,
        type=transaction.type,
        user_id=current_user.id,
        wallet_id=transaction.wallet_id,
        category_id=transaction.category_id
    )

    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)

    return new_transaction


@router.get("/", response_model=list[TransactionResponse])
async def get_transactions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Transaction).where(Transaction.user_id == current_user.id)
    )
    return result.scalars().all()