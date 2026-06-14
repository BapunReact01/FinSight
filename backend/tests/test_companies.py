def test_create_company(client, auth_headers):
    company_data = {
        "company_name": "Tech Corp",
        "industry": "Technology"
    }
    response = client.post("/companies/", json=company_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["company_name"] == "Tech Corp"
    assert data["industry"] == "Technology"
    assert "id" in data


def test_get_companies(client, auth_headers):
    # Create a company first
    company_data = {
        "company_name": "Test Company",
        "industry": "Finance"
    }
    client.post("/companies/", json=company_data, headers=auth_headers)
    
    response = client.get("/companies/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_get_company_by_id(client, auth_headers):
    company_data = {
        "company_name": "Specific Company",
        "industry": "Healthcare"
    }
    create_response = client.post("/companies/", json=company_data, headers=auth_headers)
    company_id = create_response.json()["id"]
    
    response = client.get(f"/companies/{company_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["company_name"] == "Specific Company"


def test_update_company(client, auth_headers):
    company_data = {
        "company_name": "Old Name",
        "industry": "Retail"
    }
    create_response = client.post("/companies/", json=company_data, headers=auth_headers)
    company_id = create_response.json()["id"]
    
    update_data = {
        "company_name": "New Name",
        "industry": "Technology"
    }
    response = client.put(f"/companies/{company_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["company_name"] == "New Name"


def test_delete_company(client, auth_headers):
    company_data = {
        "company_name": "To Delete",
        "industry": "Manufacturing"
    }
    create_response = client.post("/companies/", json=company_data, headers=auth_headers)
    company_id = create_response.json()["id"]
    
    response = client.delete(f"/companies/{company_id}", headers=auth_headers)
    assert response.status_code == 204  # Changed from 200 to 204
    
    # Verify deletion
    get_response = client.get(f"/companies/{company_id}", headers=auth_headers)
    assert get_response.status_code == 404