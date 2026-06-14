import pandas as pd
from typing import List, Dict
from datetime import datetime

def parse_csv_file(file_content: bytes) -> List[Dict]:
    """Parse CSV file and return list of dictionaries"""
    try:
        df = pd.read_csv(file_content)
        return df.to_dict('records')
    except Exception as e:
        raise ValueError(f"Error parsing CSV: {str(e)}")

def parse_excel_file(file_content: bytes) -> List[Dict]:
    """Parse Excel file and return list of dictionaries"""
    try:
        df = pd.read_excel(file_content)
        return df.to_dict('records')
    except Exception as e:
        raise ValueError(f"Error parsing Excel: {str(e)}")

def parse_csv(file_content) -> List[Dict]:
    """Parse CSV file from StringIO/BytesIO and return list of dictionaries"""
    try:
        df = pd.read_csv(file_content)
        return df.to_dict('records')
    except Exception as e:
        raise ValueError(f"Error parsing CSV: {str(e)}")

def parse_excel(file_content) -> List[Dict]:
    """Parse Excel file from BytesIO and return list of dictionaries"""
    try:
        df = pd.read_excel(file_content)
        return df.to_dict('records')
    except Exception as e:
        raise ValueError(f"Error parsing Excel: {str(e)}")

def validate_transaction_data(data: Dict) -> bool:
    """Validate transaction data structure"""
    required_fields = ['date', 'category', 'amount', 'transaction_type']
    return all(field in data for field in required_fields)