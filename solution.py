def validate_password(password: str) -> dict:
    """
    Validates a password based on several security criteria:
    - At least 8 characters long
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character from the set: !@#$%^&*

    Returns a dictionary containing validation status, strength, and a list of error messages.
    """
    errors = []
    criteria_met = 0
    special_characters = "!@#$%^&*"

    # Check 1: Length
    if len(password) >= 8:
        criteria_met += 1
    else:
        errors.append("Password must be at least 8 characters long.")

    # Check 2: Uppercase
    if any(c.isupper() for c in password):
        criteria_met += 1
    else:
        errors.append("Password must contain at least one uppercase letter.")

    # Check 3: Lowercase
    if any(c.islower() for c in password):
        criteria_met += 1
    else:
        errors.append("Password must contain at least one lowercase letter.")

    # Check 4: Digit
    if any(c.isdigit() for c in password):
        criteria_met += 1
    else:
        errors.append("Password must contain at least one digit.")

    # Check 5: Special character
    if any(c in special_characters for c in password):
        criteria_met += 1
    else:
        errors.append("Password must contain at least one special character (!@#$%^&*).")

    is_valid = len(errors) == 0

    # Strength mapping based on how many of the 5 criteria are satisfied
    if criteria_met == 5:
        strength = "Strong"
    elif criteria_met >= 3:
        strength = "Medium"
    else:
        strength = "Weak"

    return {
        "is_valid": is_valid,
        "strength": strength,
        "errors": errors
    }
