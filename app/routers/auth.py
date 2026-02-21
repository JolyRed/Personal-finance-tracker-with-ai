from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from app.models.users import User
from app.utils.database import AsyncSession
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.utils.database import get_db
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.utils.dependencies import get_current_user
from app.utils.security import create_access_token, create_refresh_token
from app.schemas.token import TokenResponse, RefreshRequest

from datetime import timedelta


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await db.execute(select(User).where(User.email == user.email))
    if db_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Такой email уже зарегистрирован")
    
    hashed_password = hash_password(user.password)
    
    new_user = User(email=user.email, hashed_password=hashed_password, username=user.username)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
   
@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await db.execute(select(User).where(User.email == user.email))
    db_user = db_user.scalar_one_or_none()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    
    access_token = create_access_token({"user_id": db_user.id, "username": db_user.username, "email": db_user.email}, expires_delta=timedelta(minutes=30))
    refresh_token = create_refresh_token({"user_id": db_user.id})


    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/refresh")
async def refresh_access_token(request: RefreshRequest, db: AsyncSession = Depends(get_db)) -> dict:
    """Обновить access_token с помощью refresh_token
    
    Refresh token действует 7 дней, access token перевыпускается на 30 минут
    """

    # расшифровка refresh token
    payload = decode_token(request.refresh_token)

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный или истёкший refresh token")

    # проверка, что это именно refresh
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Это не refresh token")

    # получаем user_id
    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некоррекнтый токен")

    # находим пользователя в бд
    user = await db.execute(select(User).where(User.id == user_id))
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    # создание нового access_token
    new_access_token = create_access_token(
        data={"user_id": user.id,
              "email": user.email,
              "is_admin": user.is_admin},
              expires_delta=timedelta(minutes=30)
    )
    

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }