from app.utils.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.models.users import User
from app.models.wallets import Wallet
from app.models.categories import Category

class Income(Base):
    __tablename__ = 'incomes'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    wallet_id = Column(Integer, ForeignKey('wallets.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    user = relationship("User", back_populates="incomes")
    wallet = relationship("Wallet", back_populates="incomes")
    category = relationship("Category", back_populates="incomes")
    