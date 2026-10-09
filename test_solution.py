from solution import validate_password

def test_valid_password():
    assert validate_password("SecurePass123") is True
    assert validate_password("AbcdeF9!") is True

def test_too_short():
    assert validate_password("Ab1") is False

def test_missing_upper():
    assert validate_password("securepass123") is False

def test_missing_lower():
    assert validate_password("SECUREPASS123") is False

def test_missing_digit():
    assert validate_password("SecurePass") is False

def test_forbidden_words():
    # Case-insensitive checks for forbidden substrings
    assert validate_password("MyPassword1") is False
    assert validate_password("mypassword1") is False
    assert validate_password("PASSWORD123") is False
    assert validate_password("AdminSecure2") is False
    assert validate_password("123456Abc") is False
    assert validate_password("Abc123456") is False