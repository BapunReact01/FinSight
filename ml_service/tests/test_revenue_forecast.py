import pytest
import pandas as pd
from models.revenue_forecast import RevenueForecaster


def test_revenue_forecaster_initialization():
    forecaster = RevenueForecaster()
    assert forecaster is not None
    assert forecaster.model is None


@pytest.mark.skip(reason="Prophet version compatibility issue with stan_backend")
def test_revenue_forecaster_train():
    forecaster = RevenueForecaster()
    
    data = pd.DataFrame({
        'transaction_date': pd.date_range(start='2023-01-01', periods=12, freq='M'),
        'amount': [10000, 12000, 15000, 18000, 20000, 22000,
                   25000, 28000, 30000, 32000, 35000, 38000],
        'transaction_type': ['income'] * 12
    })
    
    forecaster.train(data)
    assert forecaster.model is not None


@pytest.mark.skip(reason="Prophet version compatibility issue with stan_backend")
def test_revenue_forecaster_predict():
    forecaster = RevenueForecaster()
    
    data = pd.DataFrame({
        'transaction_date': pd.date_range(start='2023-01-01', periods=12, freq='M'),
        'amount': [10000, 12000, 15000, 18000, 20000, 22000,
                   25000, 28000, 30000, 32000, 35000, 38000],
        'transaction_type': ['income'] * 12
    })
    forecaster.train(data)
    
    forecast = forecaster.predict(periods=3)
    assert forecast is not None
    assert len(forecast) == 3


@pytest.mark.skip(reason="Prophet version compatibility issue with stan_backend")
def test_revenue_forecaster_insufficient_data():
    forecaster = RevenueForecaster()
    
    data = pd.DataFrame({
        'transaction_date': pd.date_range(start='2023-01-01', periods=1, freq='M'),
        'amount': [10000],
        'transaction_type': ['income']
    })
    
    with pytest.raises(ValueError):
        forecaster.train(data)