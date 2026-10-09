def validate_password(password: str) -> bool:
    """
    Validates a password.
    Returns True if valid, False otherwise.
    Rules:
    - Must be at least 8 characters long.
    - Must contain at least one uppercase letter, one lowercase letter, and one digit.
    - Must not contain common words like "password", "admin", or "123456" (case-insensitive).
    """
    if len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    if not (has_upper and has_lower and has_digit):
        return False
        
    # Check for forbidden substrings (case-insensitive)
    forbidden = ["password", "admin", "123456"]
    password_lower = password.lower()
    for word in forbidden:
        if word in password_lower:
            return False
            
    return True