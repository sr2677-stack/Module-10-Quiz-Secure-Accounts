import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
import app.database as app_database  # ✅ import the module to patch it

# ✅ Single shared in-memory engine
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Patch the app's engine so Base.metadata uses OUR engine
app_database.engine = engine
app_database.SessionLocal = TestingSessionLocal

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Override dependency
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # ✅ Create all tables on our test engine
    Base.metadata.create_all(bind=engine)
    yield
    # ✅ Clean up after each test
    Base.metadata.drop_all(bind=engine)


def test_create_user():
    response = client.post("/users/", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "secret"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"
    assert "password_hash" not in data

def test_duplicate_email():
    client.post("/users/", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "secret"
    })
    response = client.post("/users/", json={
        "username": "bob",
        "email": "alice@example.com",
        "password": "secret"
    })
    assert response.status_code == 400

def test_duplicate_username():
    client.post("/users/", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "secret"
    })
    response = client.post("/users/", json={
        "username": "alice",
        "email": "other@example.com",
        "password": "secret"
    })
    assert response.status_code == 400

def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404