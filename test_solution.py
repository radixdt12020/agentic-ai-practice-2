import pytest
from solution import validate_password, calculate_strength

def test_valid_strong_password():
    result = validate_password("SuperSecure123!")
    assert result["is_valid"] is True
    assert result["strength"] == 100
    assert len(result["errors"]) == 0

def test_valid_medium_password():
    result = validate_password("Pass123!")
    assert result["is_valid"] is True
    assert result["strength"] == 90
    assert len(result["errors"]) == 0

def test_invalid_weak_password():
    result = validate_password("123")
    assert result["is_valid"] is False
    assert result["strength"] == 27
    assert len(result["errors"]) > 0

def test_invalid_medium_password():
    result = validate_password("Abcdefg1")
    assert result["is_valid"] is False
    assert result["strength"] == 77
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

def test_common_words_rejection():
    # Test case-insensitive rejection of "password"
    result1 = validate_password("MyPaSsWoRd123!")
    assert result1["is_valid"] is False
    assert "Password must not contain common words like 'password', 'admin', or '123456'." in result1["errors"]

    # Test case-insensitive rejection of "admin"
    result2 = validate_password("AdminSecure!9")
    assert result2["is_valid"] is False
    assert "Password must not contain common words like 'password', 'admin', or '123456'." in result2["errors"]

    # Test rejection of "123456"
    result3 = validate_password("Secret123456!")
    assert result3["is_valid"] is False
    assert "Password must not contain common words like 'password', 'admin', or '123456'." in result3["errors"]

def test_calculate_strength_direct():
    assert calculate_strength("SuperSecure123!") == 100
    assert calculate_strength("Pass123!") == 90
    assert calculate_strength("123") == 27
    with pytest.raises(TypeError):
        calculate_strength(12345)  # type: ignore
