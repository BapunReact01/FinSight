from datetime import date


def test_create_transaction(client, auth_headers):
    # Create a company first
    company_data = {
        "company_name": "Transaction Company",
        "industry": "Finance"
    }
    company_response = client.post("/companies/", json=company_data, headers=auth_headers)
    company_id = company_response.json()["id"]
    
    transaction_data = {
        "company_id": company_id,
        "transaction_date": "2024-01-15",
        "category": "Sales",
        "amount": 10000.00,
        "transaction_type": "income",
        "description": "Monthly sales"
    }
    response = client.post("/transactions/", json=transaction_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 10000.00
    assert data["category"] == "Sales"


def test_get_transactions(client, auth_headers):
    # Create company and transaction
    company_data = {
        "company_name": "Test Company",
        "industry": "Technology"
    }
    company_response = client.post("/companies/", json=company_data, headers=auth_headers)
    company_id = company_response.json()["id"]
    
    transaction_data = {
        "company_id": company_id,
        "transaction_date": "2024-01-15",
        "category": "Services",
        "amount": 5000.00,
        "transaction_type": "income"
    }
    client.post("/transactions/", json=transaction_data, headers=auth_headers)
    
    response = client.get("/transactions/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_get_transactions_by_company(client, auth_headers):
    company_data = {
        "company_name": "Filter Company",
        "industry": "Retail"
    }
    company_response = client.post("/companies/", json=company_data, headers=auth_headers)
    company_id = company_response.json()["id"]
    
    transaction_data = {
        "company_id": company_id,
        "transaction_date": "2024-01-20",
        "category": "Inventory",
        "amount": 3000.00,
        "transaction_type": "expense"
    }
    client.post("/transactions/", json=transaction_data, headers=auth_headers)
    
    response = client.get(f"/transactions/?company_id={company_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


#def test_update_transaction(client, auth_headers):
#   company_data = {
#       "company_name": "Update Company",
#        "industry": "Services"
#    }
#    company_response = client.post("/companies/", json=company_data, headers=auth_headers)
#    company_id = company_response.json()["id"]
    
#    transaction_data = {
#        "company_id": company_id,
#        "transaction_date": "2024-01-10",
#        "category": "Old Category",
#        "amount": 1000.00,
#        "transaction_type": "expense"
#    }
#    create_response = client.post("/transactions/", json=transaction_data, headers=auth_headers)
#    transaction_id = create_response.json()["id"]
#    
#    update_data = {
#        "amount": 1500.00,
#        "category": "New Category"
#    }
#    response = client.put(f"/transactions/{transaction_id}", json=update_data, headers=auth_headers)
#    assert response.status_code == 200
#    data = response.json()
#    assert data["amount"] == 1500.00


#def test_delete_transaction(client, auth_headers):
#    company_data = {
#        "company_name": "Delete Company",
#        "industry": "Manufacturing"
#    }
#    company_response = client.post("/companies/", json=company_data, headers=auth_headers)
#    company_id = company_response.json()["id"]
#    
#    transaction_data = {
#        "company_id": company_id,
#       "transaction_date": "2024-01-05",
#        "category": "Supplies",
#        "amount": 500.00,
#        "transaction_type": "expense"
#    }
#    create_response = client.post("/transactions/", json=transaction_data, headers=auth_headers)
#    transaction_id = create_response.json()["id"]
    
#    response = client.delete(f"/transactions/{transaction_id}", headers=auth_headers)
#    assert response.status_code == 200