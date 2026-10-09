import pytest
from solution import validate_password

def test_valid_strong_password():
    res = validate_password("Abc1234!")
    assert res["is_valid"] is True
    assert res["strength"] == "Strong"
    assert len(res["errors"]) == 0

def test_weak_password_all_missing():
    res = validate_password("")
    assert res["is_valid"] is False
    assert res["strength"] == "Weak"
    assert len(res["errors"]) == 5

def test_medium_password_missing_some_rules():
    # Meets length, uppercase, lowercase. Missing digit and special. (Score 3 -> Medium)
    res = validate_password("Abcdefgh")
    assert res["is_valid"] is False
    assert res["strength"] == "Medium"
    assert len(res["errors"]) == 2
    assert "Password must contain at least one digit." in res["errors"]
    assert "Password must contain at least one special character (!@#$%^&*)." in res["errors"]

def test_password_missing_special():
    # Meets length, upper, lower, digit. Missing special. (Score 4 -> Medium)
    res = validate_password("Abc12345")
    assert res["is_valid"] is False
    assert res["strength"] == "Medium"
    assert len(res["errors"]) == 1
    assert "Password must contain at least one special character (!@#$%^&*)." in res["errors"]

def test_password_short_but_has_other_types():
    # Meets upper, lower, digit, special. Missing length. (Score 4 -> Medium)
    res = validate_password("Ab1!")
    assert res["is_valid"] is False
    assert res["strength"] == "Medium"
    assert len(res["errors"]) == 1
    assert "Password must be at least 8 characters long." in res["errors"]

def test_invalid_input_type():
    res = validate_password(12345678)  # type: ignore
    assert res["is_valid"] is False
    assert res["strength"] == "Weak"
    assert "Password must be a string." in res["errors"]
