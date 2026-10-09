import pytest
from solution import validate_password

def test_valid_strong_password():
    result = validate_password("P@ssword123")
    assert result["is_valid"] is True
    assert result["strength"] == "Strong"
    assert len(result["errors"]) == 0

def test_weak_password_short_and_simple():
    result = validate_password("abc")
    assert result["is_valid"] is False
    assert result["strength"] == "Weak"
    assert "Password must be at least 8 characters long." in result["errors"]
    assert "Password must contain at least one uppercase letter." in result["errors"]
    assert "Password must contain at least one digit." in result["errors"]
    assert "Password must contain at least one special character (!@#$%^&*)." in result["errors"]

def test_medium_password_missing_special():
    # Has length (8), uppercase, lowercase, digits, but NO special character
    result = validate_password("Abc12345")
    assert result["is_valid"] is False
    assert result["strength"] == "Medium"
    assert len(result["errors"]) == 1
    assert "Password must contain at least one special character (!@#$%^&*)." in result["errors"]

def test_medium_password_missing_digit():
    # Has length (10), uppercase, lowercase, special character, but NO digit
    result = validate_password("Abcdefg@hi")
    assert result["is_valid"] is False
    assert result["strength"] == "Medium"
    assert len(result["errors"]) == 1
    assert "Password must contain at least one digit." in result["errors"]

def test_empty_password():
    result = validate_password("")
    assert result["is_valid"] is False
    assert result["strength"] == "Weak"
    assert len(result["errors"]) == 5

def test_special_characters_outside_allowed_set():
    # Uses ')' which is a special character but not in !@#$%
    result = validate_password("Password123)")
    assert result["is_valid"] is False
    assert "Password must contain at least one special character (!@#$%^&*)." in result["errors"]
