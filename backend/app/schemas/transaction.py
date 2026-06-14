from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class TransactionBase(BaseModel):
    company_id: int
    transaction_date: date
    category: str
    amount: float
    transaction_type: str
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True