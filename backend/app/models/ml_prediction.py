from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Date
from sqlalchemy.sql import func
from app.core.database import Base

class MLPrediction(Base):
    __tablename__ = "ml_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    prediction_date = Column(Date, nullable=False)
    predicted_revenue = Column(Numeric(15, 2), nullable=False)
    confidence_score = Column(Numeric(5, 2), nullable=False)
    model_type = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())