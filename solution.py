def validate_password(password: str) -> dict:
    """
    Validates a password based on several criteria and determines its strength.
    
    Criteria:
    - At least 8 characters long
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character from the set: !@#$%^&*
    
    Returns a dictionary:
    {
        "is_valid": bool,
        "strength": "Weak" | "Medium" | "Strong",
        "errors": list[str]
    }
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string")

    errors = []
    
    # Evaluate individual criteria
    has_len = len(password) >= 8
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    special_chars = "!@#$%^&*"
    has_special = any(c in special_chars for c in password)
    
    # Collect errors
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
        
    is_valid = len(errors) == 0
    
    # Strength metric based on criteria score (0 to 5 points)
    score = sum([has_len, has_upper, has_lower, has_digit, has_special])
    
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"
        
    return {
        "is_valid": is_valid,
        "strength": strength,
        "errors": errors
    }
