def validate_password(password: str) -> dict:
    if not isinstance(password, str):
        return {
            "is_valid": False,
            "strength": "Weak",
            "errors": ["Password must be a string."]
        }
    
    errors = []
    score = 0
    
    # 1. Length check
    if len(password) >= 8:
        score += 1
    else:
        errors.append("Password must be at least 8 characters long.")
        
    # 2. Uppercase check
    if any(c.isupper() for c in password):
        score += 1
    else:
        errors.append("Password must contain at least one uppercase letter.")
        
    # 3. Lowercase check
    if any(c.islower() for c in password):
        score += 1
    else:
        errors.append("Password must contain at least one lowercase letter.")
        
    # 4. Digit check
    if any(c.isdigit() for c in password):
        score += 1
    else:
        errors.append("Password must contain at least one digit.")
        
    # 5. Special character check (!@#$%^&*)
    special_chars = set("!@#$%^&*")
    if any(c in special_chars for c in password):
        score += 1
    else:
        errors.append("Password must contain at least one special character (!@#$%^&*).")
        
    is_valid = len(errors) == 0
    
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
