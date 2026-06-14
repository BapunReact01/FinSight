import pytest
import pandas as pd
from models.anomaly_detection import ExpenseAnomalyDetector


def test_anomaly_detector_initialization():
    detector = ExpenseAnomalyDetector()
    assert detector is not None
    assert detector.model is not None


def test_anomaly_detector_train():
    detector = ExpenseAnomalyDetector()
    
    # Create sample data with transaction_type and category
    data = pd.DataFrame({
        'transaction_date': pd.date_range(start='2023-01-01', periods=20, freq='D'),
        'amount': [1000, 1100, 1050, 1200, 1150, 1300, 1250, 1400,
                   1350, 1500, 1450, 1600, 1550, 1700, 1650, 1800,
                   5000, 1750, 1900, 1850],
        'transaction_type': ['expense'] * 20,
        'category': ['Office'] * 10 + ['Travel'] * 5 + ['Supplies'] * 5
    })
    
    detector.train(data)
    assert detector.model is not None


def test_anomaly_detector_detect():
    detector = ExpenseAnomalyDetector()
    
    # Train with sample data
    data = pd.DataFrame({
        'transaction_date': pd.date_range(start='2023-01-01', periods=20, freq='D'),
        'amount': [1000, 1100, 1050, 1200, 1150, 1300, 1250, 1400,
                   1350, 1500, 1450, 1600, 1550, 1700, 1650, 1800,
                   5000, 1750, 1900, 1850],
        'transaction_type': ['expense'] * 20,
        'category': ['Office'] * 10 + ['Travel'] * 5 + ['Supplies'] * 5
    })
    detector.train(data)
    
    # Detect anomalies
    anomalies = detector.detect_anomalies(data)
    assert anomalies is not None
    assert len(anomalies) >= 1


def test_anomaly_detector_insufficient_data():
    detector = ExpenseAnomalyDetector()
    
    # Create insufficient data (less than 10 points)
    data = pd.DataFrame({
        'transaction_date': pd.date_range(start='2023-01-01', periods=5, freq='D'),
        'amount': [1000, 1100, 1050, 1200, 1150],
        'transaction_type': ['expense'] * 5,
        'category': ['Office'] * 5
    })
    
    with pytest.raises(ValueError):
        detector.train(data)