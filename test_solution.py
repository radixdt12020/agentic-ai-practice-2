import pytest
from solution import validate_password

def test_valid_strong_password():
    result = validate_password("SuperSecure123!")
    assert result["is_valid"] is True
    assert result["strength"] == "Strong"
    assert len(result["errors"]) == 0

def test_valid_medium_password():
    result = validate_password("Pass123!")
    assert result["is_valid"] is True
    assert result["strength"] == "Medium"
    assert len(result["errors"]) == 0

def test_invalid_weak_password():
    result = validate_password("123")
    assert result["is_valid"] is False
    assert result["strength"] == "Weak"
    assert len(result["errors"]) > 0

def test_invalid_medium_password():
    result = validate_password("Password123")
    assert result["is_valid"] is False
    assert result["strength"] == "Medium"
    assert "Password must contain at least one special character (!@#$%^&*)." in result["errors"]

def test_missing_uppercase():
    result = validate_password("password123!")
    assert result["is_valid"] is False
    assert "Password must contain at least one uppercase letter." in result["errors"]

def test_missing_lowercase():
    result = validate_password("PASSWORD123!")
    assert result["is_valid"] is False
    assert "Password must contain at least one lowercase letter." in result["errors"]

def test_missing_digit():
    result = validate_password("Password!!!")
    assert result["is_valid"] is False
    assert "Password must contain at least one digit." in result["errors"]

def test_non_string_input():
    with pytest.raises(TypeError):
        validate_password(12345678)  # type: ignore