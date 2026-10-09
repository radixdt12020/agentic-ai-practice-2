import pytest
from solution import reverse_string, is_palindrome


def test_reverse_string_basic():
    assert reverse_string("hello") == "olleh"
    assert reverse_string("Python") == "nohtyP"


def test_reverse_string_empty():
    assert reverse_string("") == ""


def test_reverse_string_single_char():
    assert reverse_string("a") == "a"


def test_reverse_string_unicode():
    assert reverse_string("héllo") == "olléh"
    assert reverse_string("🚀🌟") == "🌟🚀"


def test_reverse_string_invalid_type():
    with pytest.raises(TypeError):
        reverse_string(123)
    with pytest.raises(TypeError):
        reverse_string(None)


def test_is_palindrome_basic():
    assert is_palindrome("racecar") is True
    assert is_palindrome("madam") is True
    assert is_palindrome("hello") is False


def test_is_palindrome_empty_and_single_char():
    assert is_palindrome("") is True
    assert is_palindrome("a") is True


def test_is_palindrome_case_insensitivity_default():
    assert is_palindrome("RaceCar") is True
    assert is_palindrome("Madam") is True


def test_is_palindrome_case_sensitive():
    assert is_palindrome("RaceCar", case_sensitive=True) is False
    assert is_palindrome("racecar", case_sensitive=True) is True


def test_is_palindrome_ignore_whitespace():
    assert is_palindrome("nurses run") is True
    assert is_palindrome("nurses run", ignore_whitespace=False) is False


def test_is_palindrome_invalid_type():
    with pytest.raises(TypeError):
        is_palindrome(12321)
    with pytest.raises(TypeError):
        is_palindrome(None)
