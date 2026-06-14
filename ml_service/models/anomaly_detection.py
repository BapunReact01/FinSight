import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Tuple

class ExpenseAnomalyDetector:
    def __init__(self, contamination: float = 0.1):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def prepare_data(self, transactions: List[Dict]) -> pd.DataFrame:
        """Prepare transaction data for anomaly detection"""
        df = pd.DataFrame(transactions)
        
        # Filter expense transactions
        df = df[df['transaction_type'] == 'expense']
        
        # Create features
        df['amount'] = df['amount'].astype(float)
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        df['day_of_week'] = df['transaction_date'].dt.dayofweek
        df['day_of_month'] = df['transaction_date'].dt.day
        df['month'] = df['transaction_date'].dt.month
        
        # One-hot encode category
        category_dummies = pd.get_dummies(df['category'], prefix='category')
        df = pd.concat([df, category_dummies], axis=1)
        
        # Select features
        feature_cols = ['amount', 'day_of_week', 'day_of_month', 'month'] + \
                      [col for col in df.columns if col.startswith('category_')]
        
        return df[feature_cols]
    
    def train(self, transactions: List[Dict]) -> None:
        """Train the Isolation Forest model"""
        df = self.prepare_data(transactions)
        
        if len(df) < 10:
            raise ValueError("Need at least 10 transactions for training")
        
        # Scale features
        X_scaled = self.scaler.fit_transform(df)
        
        # Train model
        self.model.fit(X_scaled)
        self.is_trained = True
    
    def detect_anomalies(self, transactions: List[Dict]) -> List[Dict]:
        """Detect anomalies in expense transactions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before detection")
        
        df = pd.DataFrame(transactions)
        df = df[df['transaction_type'] == 'expense'].copy()
        
        if len(df) == 0:
            return []
        
        # Prepare features
        features = self.prepare_data(transactions)
        X_scaled = self.scaler.transform(features)
        
        # Predict anomalies
        predictions = self.model.predict(X_scaled)
        scores = self.model.score_samples(X_scaled)
        
        # Mark anomalies
        df['is_anomaly'] = predictions == -1
        df['anomaly_score'] = scores
        
        # Return only anomalies
        anomalies = df[df['is_anomaly']].to_dict('records')
        
        result = []
        for anomaly in anomalies:
            result.append({
                'transaction_id': anomaly.get('id'),
                'amount': float(anomaly['amount']),
                'category': anomaly['category'],
                'transaction_date': str(anomaly['transaction_date']),
                'anomaly_score': round(anomaly['anomaly_score'], 4),
                'reason': 'Unusual spending pattern detected'
            })
        
        return result
    
    def get_confidence_score(self) -> float:
        """Calculate confidence score based on model fit"""
        if not self.is_trained:
            return 0.0
        
        # Simple confidence based on contamination parameter
        return 0.80  # Placeholder