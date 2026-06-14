from flask import Flask, request, jsonify
from models.revenue_forecast import RevenueForecaster
from models.anomaly_detection import ExpenseAnomalyDetector
from utils.database import get_company_transactions, save_ml_prediction
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    """Show available endpoints"""
    return jsonify({
        'service': 'FinSight ML Service',
        'version': '1.0.0',
        'endpoints': {
            'GET /': 'Service information',
            'GET /health': 'Health check',
            'POST /forecast/<company_id>': 'Revenue forecasting',
            'POST /anomalies/<company_id>': 'Expense anomaly detection'
        },
        'usage': {
            'forecast': {'body': {'periods': 30}},
            'anomalies': {'body': {}}
        }
    })

@app.route('/forecast/<int:company_id>', methods=['POST'])
def forecast_revenue(company_id):
    """Generate revenue forecast for a company"""
    try:
        data = request.json
        periods = data.get('periods', 30)
        
        # Get transactions
        transactions = get_company_transactions(company_id)
        
        # Train model
        forecaster = RevenueForecaster()
        forecaster.train(transactions)
        
        # Generate forecast
        predictions = forecaster.forecast(periods)
        confidence = forecaster.get_confidence_score()
        
        # Save predictions to database
        for pred in predictions:
            save_ml_prediction(
                company_id=company_id,
                prediction_date=pred['date'],
                predicted_revenue=pred['predicted_revenue'],
                confidence_score=confidence,
                model_type='revenue_forecast'
            )
        
        return jsonify({
            'company_id': company_id,
            'predictions': predictions,
            'confidence_score': confidence,
            'model_type': 'revenue_forecast'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/anomalies/<int:company_id>', methods=['POST'])
def detect_anomalies(company_id):
    """Detect expense anomalies for a company"""
    try:
        # Get transactions
        transactions = get_company_transactions(company_id)
        
        # Train model
        detector = ExpenseAnomalyDetector()
        detector.train(transactions)
        
        # Detect anomalies
        anomalies = detector.detect_anomalies(transactions)
        confidence = detector.get_confidence_score()
        
        return jsonify({
            'company_id': company_id,
            'anomalies': anomalies,
            'anomaly_count': len(anomalies),
            'confidence_score': confidence,
            'model_type': 'anomaly_detection'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)