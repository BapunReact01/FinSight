from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Date
from sqlalchemy.sql import func
from app.core.database import Base

class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    transaction_date = Column(Date, nullable=False)
    category = Column(String(100), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    transaction_type = Column(String(50), nullable=False)  # income, expense
    description = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())