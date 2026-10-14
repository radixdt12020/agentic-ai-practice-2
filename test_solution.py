import pytest
from solution import validate_registration_payload, RegistrationValidationError


def test_valid_registration_payload():
    payload = {
        "username": "alice",
        "email": "alice@example.com",
        "age": 25
    }
    result = validate_registration_payload(payload)
    assert result == payload


def test_minimum_valid_age():
    payload = {
        "username": "bob",
        "email": "bob@example.com",
        "age": 18
    }
    result = validate_registration_payload(payload)
    assert result["age"] == 18


def test_underage_user_raises_validation_error():
    payload = {
        "username": "minor",
        "email": "minor@example.com",
        "age": 17
    }
    with pytest.raises(RegistrationValidationError, match="at least 18 years old"):
        validate_registration_payload(payload)


@pytest.mark.parametrize("missing_key", ["username", "email", "age"])
def test_missing_required_fields_raises_validation_error(missing_key):
    payload = {
        "username": "user",
        "email": "user@example.com",
        "age": 20
    }
    payload.pop(missing_key)
    with pytest.raises(RegistrationValidationError, match=f"Missing required field: '{missing_key}'"):
        validate_registration_payload(payload)


@pytest.mark.parametrize("invalid_email", ["invalid", "user@", "@example.com", "user@domain", 123])
def test_invalid_email_raises_validation_error(invalid_email):
    payload = {
        "username": "user",
        "email": invalid_email,
        "age": 30
    }
    with pytest.raises(RegistrationValidationError, match="Email must be a valid email address"):
        validate_registration_payload(payload)


@pytest.mark.parametrize("invalid_username", ["", "   ", 123, None])
def test_invalid_username_raises_validation_error(invalid_username):
    payload = {
        "username": invalid_username,
        "email": "user@example.com",
        "age": 30
    }
    with pytest.raises(RegistrationValidationError, match="Username must be a non-empty string"):
        validate_registration_payload(payload)


@pytest.mark.parametrize("invalid_age", ["18", 18.5, True, False, None])
def test_invalid_age_type_raises_validation_error(invalid_age):
    payload = {
        "username": "user",
        "email": "user@example.com",
        "age": invalid_age
    }
    with pytest.raises(RegistrationValidationError, match="Age must be an integer"):
        validate_registration_payload(payload)


def test_non_dict_payload_raises_validation_error():
    with pytest.raises(RegistrationValidationError, match="Payload must be a dictionary"):
        validate_registration_payload(["username", "email", "age"])
