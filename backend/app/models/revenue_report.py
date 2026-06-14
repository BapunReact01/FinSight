from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Date, UniqueConstraint
from sqlalchemy.sql import func
from app.core.database import Base

class RevenueReport(Base):
    __tablename__ = "revenue_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    report_month = Column(Date, nullable=False)
    total_revenue = Column(Numeric(15, 2), nullable=False)
    total_expenses = Column(Numeric(15, 2), nullable=False)
    profit = Column(Numeric(15, 2), nullable=False)
    growth_rate = Column(Numeric(5, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (UniqueConstraint('company_id', 'report_month', name='unique_company_month'),)