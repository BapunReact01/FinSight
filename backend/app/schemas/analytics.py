from pydantic import BaseModel
from typing import Optional

class RevenueDashboard(BaseModel):
    total_revenue: float
    growth: float
    best_month: str
    worst_month: Optional[str] = None

class ExpenseAnalysis(BaseModel):
    highest_category: str
    amount: float
    total_expenses: float

class MonthlyReport(BaseModel):
    month: str
    revenue: float
    expenses: float
    profit: float