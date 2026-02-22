from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.categories import Category


async def seed_default_categories(db: AsyncSession):
    """Создать базовые категории (доступны всем)"""

    default_categories = [
        # Доходы
        {"name": "Зарплата", "type": "income", "icon": "💼", "is_default": True, "user_id": None},
        {"name": "Фриланс", "type": "income", "icon": "💻", "is_default": True, "user_id": None},
        {"name": "Подработка", "type": "income", "icon": "💰", "is_default": True, "user_id": None},

        # Расходы
        {"name": "Продукты", "type": "expense", "icon": "🛒", "is_default": True, "user_id": None},
        {"name": "Транспорт", "type": "expense", "icon": "🚗", "is_default": True, "user_id": None},
        {"name": "Жильё", "type": "expense", "icon": "🏠", "is_default": True, "user_id": None},
        {"name": "Развлечения", "type": "expense", "icon": "🎮", "is_default": True, "user_id": None},
        {"name": "Здоровье", "type": "expense", "icon": "💊", "is_default": True, "user_id": None},
    ]

    for cat_data in default_categories:
        result = await db.execute(
            select(Category).where(
                Category.name == cat_data["name"],
                Category.is_default == True
            )
        )
        if not result.scalar_one_or_none():
            category = Category(**cat_data)
            db.add(category)

    await db.commit()
    print("✅ Дефолтные категории созданы")