import io


def test_upload_csv_file(client, auth_headers):
    company_data = {
        "company_name": "File Company",
        "industry": "Technology"
    }
    company_response = client.post("/companies/", json=company_data, headers=auth_headers)
    company_id = company_response.json()["id"]
    
    csv_content = """transaction_date,category,amount,transaction_type,description
2024-01-15,Sales,10000.00,income,Test sale
2024-01-16,Expenses,5000.00,expense,Test expense"""
    
    files = {"file": ("test.csv", io.BytesIO(csv_content.encode()), "text/csv")}
    response = client.post(f"/files/upload?company_id={company_id}", files=files, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert "file_name" in data  # Changed from filename to file_name
    assert "file_id" in data


def test_upload_invalid_file_type(client, auth_headers):
    company_data = {
        "company_name": "Invalid File Company",
        "industry": "Retail"
    }
    company_response = client.post("/companies/", json=company_data, headers=auth_headers)
    company_id = company_response.json()["id"]
    
    files = {"file": ("test.txt", io.BytesIO(b"invalid content"), "text/plain")}
    response = client.post(f"/files/upload?company_id={company_id}", files=files, headers=auth_headers)
    assert response.status_code == 400


def test_list_files(client, auth_headers):
    response = client.get("/files/list", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "files" in data
    assert isinstance(data["files"], list)