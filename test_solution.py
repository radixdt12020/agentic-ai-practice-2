import pytest
from solution import validate_password

def test_valid_passwords():
    assert validate_password("SecurePass123!") is True
    assert validate_password("MySuperSecretKey") is True

def test_too_short():
    assert validate_password("Short1") is False

def test_forbidden_words():
    # Case-insensitive checks for forbidden substrings
    assert validate_password("MyPassword123") is False
    assert validate_password("mypassword123") is False
    assert validate_password("AdminUser2023") is False
    assert validate_password("superadmin") is False
    assert validate_password("safe1234567") is False
    assert validate_password("123456") is False

def test_invalid_types():
    assert validate_password(None) is False
    assert validate_password(12345678) is False
