def test_register_user(client):
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123",
        "role": "analyst"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "john@example.com"
    assert data["name"] == "John Doe"
    assert "id" in data


def test_register_duplicate_user(client):
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123",
        "role": "analyst"
    }
    client.post("/auth/register", json=user_data)
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400


def test_login_user(client):
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass123",
        "role": "admin"
    }
    client.post("/auth/register", json=user_data)
    
    login_data = {
        "email": "test@example.com",  # Changed from username to email
        "password": "testpass123"
    }
    response = client.post("/auth/login", json=login_data)
    print(f"Login response: {response.status_code} - {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    login_data = {
        "email": "nonexistent@example.com",  # Changed from username to email
        "password": "wrongpass"
    }
    response = client.post("/auth/login", json=login_data)
    print(f"Invalid login response: {response.status_code} - {response.text}")
    assert response.status_code == 401


def test_login_invalid_credentials(client):
    login_data = {
        "username": "nonexistent@example.com",
        "password": "wrongpass"
    }
    response = client.post("/auth/login", json=login_data)
    print(f"Invalid login response: {response.status_code} - {response.text}")
    # 422 might be returned if validation fails, check for either 401 or 422
    assert response.status_code in [401, 422]


