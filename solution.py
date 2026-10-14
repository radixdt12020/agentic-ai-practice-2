# ARCHITECTURE COMPLIANT: AGENTS.MD v1.0
from typing import Any, Dict
import re


class RegistrationValidationError(Exception):
    """Custom domain exception raised when registration payload validation fails."""
    pass


EMAIL_REGEX: re.Pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def validate_registration_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validates user registration payload ensuring required fields and constraints.

    Args:
        payload (Dict[str, Any]): Dictionary containing registration details,
            expected to have 'username', 'email', and 'age'.

    Returns:
        Dict[str, Any]: The validated payload dictionary.

    Raises:
        RegistrationValidationError: If the payload is invalid, missing required fields,
            or contains values failing business constraints (e.g., age under 18).
    """
    if not isinstance(payload, dict):
        raise RegistrationValidationError("Payload must be a dictionary.")

    required_fields = ("username", "email", "age")
    for field in required_fields:
        if field not in payload:
            raise RegistrationValidationError(f"Missing required field: '{field}'.")

    username = payload["username"]
    if not isinstance(username, str) or not username.strip():
        raise RegistrationValidationError("Username must be a non-empty string.")

    email = payload["email"]
    if not isinstance(email, str) or not EMAIL_REGEX.match(email):
        raise RegistrationValidationError("Email must be a valid email address string.")

    age = payload["age"]
    if not isinstance(age, int) or isinstance(age, bool):
        raise RegistrationValidationError("Age must be an integer.")

    if age < 18:
        raise RegistrationValidationError("User must be at least 18 years old.")

    return payload
