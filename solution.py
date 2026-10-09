def validate_password(password: str) -> bool:
    """
    Validates a password based on the following rules:
    - Must be a string.
    - Must be at least 8 characters long.
    - Must not contain common forbidden words (case-insensitive): "password", "admin", "123456".
    """
    if not isinstance(password, str):
        return False
    
    if len(password) < 8:
        return False
        
    forbidden_substrings = ["password", "admin", "123456"]
    password_lower = password.lower()
    
    for forbidden in forbidden_substrings:
        if forbidden in password_lower:
            return False
            
    return True
