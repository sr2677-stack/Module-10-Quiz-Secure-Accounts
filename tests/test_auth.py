import pytest
from app.auth import hash_password, verify_password
from app.schemas import UserCreate

# --- Password Hashing Tests ---

def test_hash_is_not_plaintext():
    hashed = hash_password("mysecret")
    assert hashed != "mysecret"
    assert isinstance(hashed, str)

def test_verify_correct_password():
    hashed = hash_password("mysecret")
    assert verify_password("mysecret", hashed) is True

def test_verify_wrong_password():
    hashed = hash_password("mysecret")
    assert verify_password("wrongpass", hashed) is False

def test_hash_different_each_time():
    # bcrypt generates different salt each time
    hash1 = hash_password("mysecret")
    hash2 = hash_password("mysecret")
    assert hash1 != hash2

# --- Schema Validation Tests ---

def test_user_create_schema_valid():
    user = UserCreate(username="alice", email="alice@example.com", password="pass123")
    assert user.username == "alice"
    assert user.email == "alice@example.com"

def test_user_create_schema_invalid_email():
    with pytest.raises(Exception):
        UserCreate(username="alice", email="not-an-email", password="pass123")

def test_user_create_schema_missing_password():
    with pytest.raises(Exception):
        UserCreate(username="alice", email="alice@example.com")

def test_user_create_schema_missing_username():
    with pytest.raises(Exception):
        UserCreate(email="alice@example.com", password="pass123")