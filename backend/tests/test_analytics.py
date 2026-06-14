from datetime import date


def test_revenue_dashboard(client, auth_headers):
    # Create company and transactions
    company_data = {
        "company_name": "Analytics Company",
        "industry": "Technology"
    }
    company_response = client.post("/companies/", json=company_data, headers=auth_headers)
    company_id = company_response.json()["id"]
    
    # Add income transactions
    for i in range(5):
        transaction_data = {
            "company_id": company_id,
            "transaction_date": f"2024-01-{10+i:02d}",
            "category": "Sales",
            "amount": 10000.00 + (i * 1000),
            "transaction_type": "income"
        }
        client.post("/transactions/", json=transaction_data, headers=auth_headers)
    
    response = client.get(f"/analytics/revenue?company_id={company_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_revenue" in data


def test_expense_analysis(client, auth_headers):
    company_data = {
        "company_name": "Expense Company",
        "industry": "Retail"
    }
    company_response = client.post("/companies/", json=company_data, headers=auth_headers)
    company_id = company_response.json()["id"]
    
    # Add expense transactions
    categories = ["Rent", "Utilities", "Supplies", "Payroll"]
    for category in categories:
        transaction_data = {
            "company_id": company_id,
            "transaction_date": "2024-01-15",
            "category": category,
            "amount": 5000.00,
            "transaction_type": "expense"
        }
        client.post("/transactions/", json=transaction_data, headers=auth_headers)
    
    response = client.get(f"/analytics/expenses?company_id={company_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_expenses" in data


def test_monthly_report(client, auth_headers):
    company_data = {
        "company_name": "Report Company",
        "industry": "Finance"
    }
    company_response = client.post("/companies/", json=company_data, headers=auth_headers)
    company_id = company_response.json()["id"]
    
    # Add transactions for a month
    transaction_data = {
        "company_id": company_id,
        "transaction_date": "2024-01-15",
        "category": "Sales",
        "amount": 20000.00,
        "transaction_type": "income"
    }
    client.post("/transactions/", json=transaction_data, headers=auth_headers)
    
    expense_data = {
        "company_id": company_id,
        "transaction_date": "2024-01-15",
        "category": "Operations",
        "amount": 5000.00,
        "transaction_type": "expense"
    }
    client.post("/transactions/", json=expense_data, headers=auth_headers)
    
    response = client.get(f"/analytics/monthly?company_id={company_id}&year=2024", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)