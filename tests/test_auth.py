import pytest
from app.auth import hash_password, verify_password
from app.schemas import UserCreate

def test_hash_is_not_plaintext():
    hashed = hash_password("mysecret")
    assert hashed != "mysecret"

def test_verify_correct_password():
    hashed = hash_password("mysecret")
    assert verify_password("mysecret", hashed) is True

def test_verify_wrong_password():
    hashed = hash_password("mysecret")
    assert verify_password("wrongpass", hashed) is False

def test_user_create_schema_valid():
    user = UserCreate(username="alice", email="alice@example.com", password="pass123")
    assert user.username == "alice"

def test_user_create_schema_invalid_email():
    with pytest.raises(Exception):
        UserCreate(username="alice", email="not-an-email", password="pass123")