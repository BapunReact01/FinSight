import psycopg2
from decouple import config
from typing import List, Dict

def get_db_connection():
    """Get PostgreSQL database connection"""
    return psycopg2.connect(
        dbname=config('DB_NAME', default='finsight_db'),
        user=config('DB_USER', default='postgres'),
        password=config('DB_PASSWORD', default='Bapun@0108'),
        host=config('DB_HOST', default='localhost'),
        port=config('DB_PORT', default='5432')
    )

def get_company_transactions(company_id: int) -> List[Dict]:
    """Get all transactions for a company"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, company_id, transaction_date, category, amount, 
               transaction_type, description
        FROM financial_transactions
        WHERE company_id = %s
        ORDER BY transaction_date
    """, (company_id,))
    
    columns = [desc[0] for desc in cursor.description]
    transactions = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return transactions

def save_ml_prediction(company_id: int, prediction_date: str, 
                      predicted_revenue: float, confidence_score: float,
                      model_type: str) -> None:
    """Save ML prediction to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO ml_predictions 
        (company_id, prediction_date, predicted_revenue, confidence_score, model_type)
        VALUES (%s, %s, %s, %s, %s)
    """, (company_id, prediction_date, predicted_revenue, confidence_score, model_type))
    
    conn.commit()
    cursor.close()
    conn.close()