from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from datetime import date, datetime
from app.core.database import get_db
from app.models.transaction import FinancialTransaction
from app.schemas.analytics import RevenueDashboard, ExpenseAnalysis, MonthlyReport
from app.dependencies import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/revenue", response_model=RevenueDashboard)
def get_revenue_dashboard(
    company_id: Optional[int] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Filter by user's company if not admin
    if current_user.role != "admin" and current_user.company_id:
        company_id = current_user.company_id
    
    # Base query for income transactions
    query = db.query(FinancialTransaction).filter(
        FinancialTransaction.transaction_type == "income"
    )
    
    if company_id:
        query = query.filter(FinancialTransaction.company_id == company_id)
    
    if year:
        query = query.filter(extract('year', FinancialTransaction.transaction_date) == year)
    
    transactions = query.all()
    
    if not transactions:
        return RevenueDashboard(
            total_revenue=0.0,
            growth=0.0,
            best_month="No data",
            worst_month=None
        )
    
    # Calculate total revenue
    total_revenue = sum(float(t.amount) for t in transactions)
    
    # Calculate revenue by month
    monthly_revenue = {}
    for t in transactions:
        month_key = t.transaction_date.strftime("%B %Y")
        monthly_revenue[month_key] = monthly_revenue.get(month_key, 0) + float(t.amount)
    
    # Find best and worst months
    if monthly_revenue:
        best_month = max(monthly_revenue, key=monthly_revenue.get)
        worst_month = min(monthly_revenue, key=monthly_revenue.get)
    else:
        best_month = "No data"
        worst_month = None
    
    # Calculate growth (compare with previous period)
    growth = 0.0
    if len(monthly_revenue) >= 2:
        months = sorted(monthly_revenue.keys())
        current = monthly_revenue[months[-1]]
        previous = monthly_revenue[months[-2]]
        if previous > 0:
            growth = ((current - previous) / previous) * 100
    
    return RevenueDashboard(
        total_revenue=total_revenue,
        growth=round(growth, 2),
        best_month=best_month,
        worst_month=worst_month
    )

@router.get("/expenses", response_model=ExpenseAnalysis)
def get_expense_analysis(
    company_id: Optional[int] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Filter by user's company if not admin
    if current_user.role != "admin" and current_user.company_id:
        company_id = current_user.company_id
    
    # Base query for expense transactions
    query = db.query(FinancialTransaction).filter(
        FinancialTransaction.transaction_type == "expense"
    )
    
    if company_id:
        query = query.filter(FinancialTransaction.company_id == company_id)
    
    if year:
        query = query.filter(extract('year', FinancialTransaction.transaction_date) == year)
    
    transactions = query.all()
    
    if not transactions:
        return ExpenseAnalysis(
            highest_category="No data",
            amount=0.0,
            total_expenses=0.0
        )
    
    # Calculate total expenses
    total_expenses = sum(float(t.amount) for t in transactions)
    
    # Calculate expenses by category
    category_expenses = {}
    for t in transactions:
        category_expenses[t.category] = category_expenses.get(t.category, 0) + float(t.amount)
    
    # Find highest spending category
    if category_expenses:
        highest_category = max(category_expenses, key=category_expenses.get)
        amount = category_expenses[highest_category]
    else:
        highest_category = "No data"
        amount = 0.0
    
    return ExpenseAnalysis(
        highest_category=highest_category,
        amount=round(amount, 2),
        total_expenses=round(total_expenses, 2)
    )

@router.get("/monthly", response_model=List[MonthlyReport])
def get_monthly_reports(
    company_id: Optional[int] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Filter by user's company if not admin
    if current_user.role != "admin" and current_user.company_id:
        company_id = current_user.company_id
    
    # Base query
    query = db.query(FinancialTransaction)
    
    if company_id:
        query = query.filter(FinancialTransaction.company_id == company_id)
    
    if year:
        query = query.filter(extract('year', FinancialTransaction.transaction_date) == year)
    
    transactions = query.all()
    
    if not transactions:
        return []
    
    # Group by month
    monthly_data = {}
    for t in transactions:
        month_key = t.transaction_date.strftime("%B %Y")
        if month_key not in monthly_data:
            monthly_data[month_key] = {"revenue": 0.0, "expenses": 0.0}
        
        if t.transaction_type == "income":
            monthly_data[month_key]["revenue"] += float(t.amount)
        else:
            monthly_data[month_key]["expenses"] += float(t.amount)
    
    # Generate monthly reports
    reports = []
    for month, data in sorted(monthly_data.items()):
        profit = data["revenue"] - data["expenses"]
        reports.append(MonthlyReport(
            month=month,
            revenue=round(data["revenue"], 2),
            expenses=round(data["expenses"], 2),
            profit=round(profit, 2)
        ))
    
    return reports