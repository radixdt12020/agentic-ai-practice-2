import pytest
from solution import validate_password

def test_valid_password():
    result = validate_password("Abcd@1234")
    assert result["is_valid"] is True
    assert result["strength"] == "Strong"
    assert len(result["errors"]) == 0

def test_short_password():
    result = validate_password("Ab@1")
    assert result["is_valid"] is False
    assert "Password must be at least 8 characters long." in result["errors"]

def test_missing_uppercase():
    result = validate_password("abcd@1234")
    assert result["is_valid"] is False
    assert "Password must contain at least one uppercase letter." in result["errors"]

def test_missing_lowercase():
    result = validate_password("ABCD@1234")
    assert result["is_valid"] is False
    assert "Password must contain at least one lowercase letter." in result["errors"]

def test_missing_digit():
    result = validate_password("Abcd@efgh")
    assert result["is_valid"] is False
    assert "Password must contain at least one digit." in result["errors"]

def test_missing_special():
    result = validate_password("Abcd12345")
    assert result["is_valid"] is False
    assert "Password must contain at least one special character (!@#$%^&*)." in result["errors"]

def test_empty_password():
    result = validate_password("")
    assert result["is_valid"] is False
    assert result["strength"] == "Weak"
    assert len(result["errors"]) == 5

def test_invalid_types():
    with pytest.raises(TypeError):
        validate_password(None)  # type: ignore
    with pytest.raises(TypeError):
        validate_password(12345)  # type: ignore

def test_strength_levels():
    # Weak (only meets 2 criteria)
    res_weak = validate_password("abcdefgh")
    assert res_weak["strength"] == "Weak"
    
    # Medium (meets 3 or 4 criteria)
    res_med = validate_password("Abcdefgh")
    assert res_med["strength"] == "Medium"
    
    # Strong (meets all 5 criteria)
    res_strong = validate_password("Abcdef1!")
    assert res_strong["strength"] == "Strong"
