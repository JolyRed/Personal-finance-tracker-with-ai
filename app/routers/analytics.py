from unicodedata import category

from fastapi import APIRouter, Depends
from sqlalchemy import select, func, extract
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transaction import Transaction
from app.models.categories import Category
from app.utils.database import get_db
from app.utils.dependencies import get_current_user
from app.models.users import User

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary")
async def get_summary(year: int, month: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    # все транзакции пользователя за текущий месяц
    result = await db.execute(select(Transaction).where(Transaction.user_id == User.id, extract('year', Transaction.date) == year, extract('month', Transaction.date) == month))

    transactions = result.scalars().all()

    if not transactions:
        return {
            "period": f"{year}-{month:02d}",
            "total_income": 0,
            "total_expense": 0,
            "balance": 0,
            "transactions_count": 0,
            "by_category": []
        }

    # считаем доходы и расходы
    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(abs(t.amount) for t in transactions if t.type == "expense")

    # группируем по категориям
    category_stats = {}
    for t in transactions:
        if t.type == 'expense' and t.category_id:
            cat_name = t.category.name if t.category else 'Без категории'
            if cat_name not in category_stats:
                category_stats[cat_name] = 0
            category_stats[cat_name] += abs(t.amount)

    by_category = []
    for cat_name, amount in category_stats.items():
        percent = (amount / total_expense * 100) if total_expense > 0 else 0
        by_category.append({
            "category": cat_name,
            "amount": amount,
            "percent": round(percent, 1)
        })

    # Сортируем по убыванию суммы
    by_category.sort(key=lambda x: x["amount"], reverse=True)

    return {
        "period": f"{year}-{month:02d}",
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense,
        "transactions_count": len(transactions),
        "by_category": by_category,
        "top_expense_category": by_category[0]["category"] if by_category else None
    }