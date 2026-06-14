import pandas as pd
import numpy as np
from prophet import Prophet
from typing import List, Dict, Tuple
from datetime import datetime, timedelta

class RevenueForecaster:
    def __init__(self):
        self.model = None
        self.is_trained = False
    
    def prepare_data(self, transactions: List[Dict]) -> pd.DataFrame:
        """Prepare transaction data for Prophet model"""
        df = pd.DataFrame(transactions)
        
        # Filter income transactions
        df = df[df['transaction_type'] == 'income']
        
        # Group by date and sum amounts
        df = df.groupby('transaction_date')['amount'].sum().reset_index()
        df.columns = ['ds', 'y']
        df['ds'] = pd.to_datetime(df['ds'])
        
        return df.sort_values('ds')
    
    def train(self, transactions: List[Dict]) -> None:
        """Train the Prophet model"""
        df = self.prepare_data(transactions)
        
        if len(df) < 2:
            raise ValueError("Need at least 2 data points for training")
        
        self.model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False
        )
        self.model.fit(df)
        self.is_trained = True
    
    def forecast(self, periods: int = 30) -> List[Dict]:
        """Generate revenue forecast for future periods"""
        if not self.is_trained:
            raise ValueError("Model must be trained before forecasting")
        
        future = self.model.make_future_dataframe(periods=periods)
        forecast = self.model.predict(future)
        
        # Return only future predictions
        forecast = forecast[forecast['ds'] > forecast['ds'].max() - pd.Timedelta(days=periods)]
        
        predictions = []
        for _, row in forecast.iterrows():
            predictions.append({
                'date': row['ds'].strftime('%Y-%m-%d'),
                'predicted_revenue': round(row['yhat'], 2),
                'lower_bound': round(row['yhat_lower'], 2),
                'upper_bound': round(row['yhat_upper'], 2)
            })
        
        return predictions
    
    def get_confidence_score(self) -> float:
        """Calculate confidence score based on model fit"""
        if not self.is_trained:
            return 0.0
        
        # Simple confidence based on data quality
        # In production, use cross-validation metrics
        return 0.85  # Placeholder