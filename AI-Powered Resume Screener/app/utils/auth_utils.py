from werkzeug.security import generate_password_hash as werkzeug_generate_password_hash
import re

def generate_password_hash(password):
    """
    Generate a password hash using Werkzeug's security functions.
    
    Args:
        password: The password to hash
        
    Returns:
        The hashed password
    """
    return werkzeug_generate_password_hash(password)

def validate_password(password):
    """
    Validate that a password meets security requirements.
    
    Args:
        password: The password to validate
        
    Returns:
        Tuple of (is_valid, message) where is_valid is a boolean and message is an error message or None
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit."
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character."
    
    return True, None

def validate_email(email):
    """
    Validate that an email address is properly formatted.
    
    Args:
        email: The email address to validate
        
    Returns:
        Tuple of (is_valid, message) where is_valid is a boolean and message is an error message or None
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        return False, "Please enter a valid email address."
    
    return True, None
