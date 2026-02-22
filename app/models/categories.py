from app.utils.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func, Boolean
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # 'income' or 'expense'
    icon = Column(String, nullable=True)  # ← ДОБАВЬ

    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    is_default = Column(Boolean, default=False)  # ← ДОБАВЬ

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")  # ← было incomes