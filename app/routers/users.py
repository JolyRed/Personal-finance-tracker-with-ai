from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from app.models.users import User
from app.utils.database import AsyncSession
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.utils.database import get_db
from app.utils.dependencies import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["users"]
)
