from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.models.categories import Category
from app.utils.database import AsyncSession
from app.schemas.categories import CategoryCreate, CategoryResponse
from app.utils.database import get_db
from app.utils.dependencies import get_current_user
from app.models.users import User


router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.post("/create", response_model=CategoryResponse)
async def create_category(
    category: CategoryCreate,
    current_user: User = Depends(get_current_user),  
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Category).where(
            Category.name == category.name,
            Category.user_id == current_user.id
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Такая категория уже существует у вас")

    new_category = Category(
        name=category.name,
        type=category.type,           
        user_id=current_user.id
    )

    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)

    return new_category
@router.get("/all", response_model=list[CategoryResponse])
async def get_all_categories(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    categories = await db.execute(select(Category))
    return categories.scalars().all()

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_name: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    category = await db.execute(select(Category).where(Category.name == category_name))
    category = category.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category

@router.delete("/{category_name}")
async def delete_category(category_name: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    category = await db.execute(select(Category).where(Category.name == category_name))
    category = category.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    await db.delete(category)
    await db.commit()
    return {"message": "Категория успешно удалена"}
