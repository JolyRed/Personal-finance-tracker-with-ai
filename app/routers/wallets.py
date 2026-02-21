from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.database import get_db
from app.utils.dependencies import get_current_user
from app.models.users import User
from app.models.wallets import Wallet
from app.schemas.wallets import WalletCreate, WalletResponse

router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.post("/create", response_model=WalletResponse)
async def create_wallet(
    wallet: WalletCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Wallet).where(
            Wallet.name == wallet.name,
            Wallet.user_id == current_user.id
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(400, "Такой кошелёк уже существует у вас")

    new_wallet = Wallet(
        name=wallet.name,
        balance=wallet.balance,
        initial_balance=wallet.initial_balance,
        currency=wallet.currency,
        user_id=current_user.id
    )

    db.add(new_wallet)
    await db.commit()
    await db.refresh(new_wallet)

    return new_wallet


@router.get("/my_wallets", response_model=list[WalletResponse])
async def get_all_wallets(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Wallet).where(Wallet.user_id == current_user.id)
    )
    wallets = result.scalars().all()

    return [WalletResponse.model_validate(w) for w in wallets]


@router.get("/{wallet_id}", response_model=WalletResponse) 
async def get_wallet(
    wallet_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Wallet).where(
            Wallet.id == wallet_id,
            Wallet.user_id == current_user.id
        )
    )
    wallet = result.scalar_one_or_none()

    if not wallet:
        raise HTTPException(404, "Кошелёк не найден")

    return wallet 


@router.delete("/{wallet_id}")
async def delete_wallet(
    wallet_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Wallet).where(
            Wallet.id == wallet_id,
            Wallet.user_id == current_user.id
        )
    )
    wallet = result.scalar_one_or_none()

    if not wallet:
        raise HTTPException(404, "Кошелёк не найден")

    await db.delete(wallet)
    await db.commit()

    return {"message": "Кошелёк успешно удалён"}