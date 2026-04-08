import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from app.main import app
from app.database import Base, get_db

TEST_DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/testdb")

engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={
        "username": "alice", "email": "alice@example.com", "password": "secret"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"
    assert "password_hash" not in data  # never expose hash

def test_duplicate_email():
    client.post("/users/", json={"username": "alice", "email": "alice@example.com", "password": "secret"})
    response = client.post("/users/", json={"username": "bob", "email": "alice@example.com", "password": "secret"})
    assert response.status_code == 400

def test_duplicate_username():
    client.post("/users/", json={"username": "alice", "email": "alice@example.com", "password": "secret"})
    response = client.post("/users/", json={"username": "alice", "email": "other@example.com", "password": "secret"})
    assert response.status_code == 400

def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404