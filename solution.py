def validate_password(password: str) -> dict:
    if not isinstance(password, str):
        raise TypeError("Password must be a string")

    errors = []
    
    has_len = len(password) >= 8
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*" for c in password)

    if not has_len:
        errors.append("Password must be at least 8 characters long.")
    if not has_upper:
        errors.append("Password must contain at least one uppercase letter.")
    if not has_lower:
        errors.append("Password must contain at least one lowercase letter.")
    if not has_digit:
        errors.append("Password must contain at least one digit.")
    if not has_special:
        errors.append("Password must contain at least one special character (!@#$%^&*).")

    # Common words check (case-insensitive)
    common_words = ["password", "admin", "123456"]
    if any(word in password.lower() for word in common_words):
        errors.append("Password must not contain common words like 'password', 'admin', or '123456'.")

    is_valid = len(errors) == 0
    score = sum([has_len, has_upper, has_lower, has_digit, has_special])

    if is_valid:
        if len(password) >= 12:
            strength = "Strong"
        else:
            strength = "Medium"
    else:
        if score >= 3:
            strength = "Medium"
        else:
            strength = "Weak"

    return {
        "is_valid": is_valid,
        "strength": strength,
        "errors": errors
    }