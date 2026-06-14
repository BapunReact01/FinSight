from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.models.transaction import FinancialTransaction
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.dependencies import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role not in ["admin", "analyst"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and analysts can create transactions"
        )
    
    db_transaction = FinancialTransaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    return db_transaction

@router.get("/", response_model=List[TransactionResponse])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    company_id: Optional[int] = None,
    transaction_type: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(FinancialTransaction)
    
    if current_user.role != "admin" and current_user.company_id:
        query = query.filter(FinancialTransaction.company_id == current_user.company_id)
    
    if company_id:
        query = query.filter(FinancialTransaction.company_id == company_id)
    
    if transaction_type:
        query = query.filter(FinancialTransaction.transaction_type == transaction_type)
    
    if start_date:
        query = query.filter(FinancialTransaction.transaction_date >= start_date)
    
    if end_date:
        query = query.filter(FinancialTransaction.transaction_date <= end_date)
    
    transactions = query.offset(skip).limit(limit).all()
    return transactions