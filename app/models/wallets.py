from app.utils.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    initial_balance = Column(Float, default=0.0)
    currency = Column(String, nullable=False, default='RUB') # e.g. 'USD', 'EUR', 'RUB'
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="wallets")
    incomes = relationship("Income", back_populates="wallet")