import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, get_db

# Test database URL (use SQLite for tests)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    # Register a test user
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass123",
        "role": "admin"
    }
    register_response = client.post("/auth/register", json=user_data)
    print(f"Register response: {register_response.status_code} - {register_response.json()}")
    
       # Login to get token
    login_data = {
        "email": "test@example.com",  # Changed from username to email
        "password": "testpass123"
    }
    response = client.post("/auth/login", json=login_data)
    print(f"Login response: {response.status_code} - {response.json()}")
    
    if response.status_code != 200:
        raise Exception(f"Login failed: {response.status_code} - {response.json()}")
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}