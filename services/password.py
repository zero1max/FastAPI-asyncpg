import bcrypt
from typing import Union

def hash_password(password: Union[str, bytes]) -> bytes:
    """
    Hash a password using bcrypt.
    
    Args:
        password: The password to hash (can be string or bytes)
        
    Returns:
        bytes: The hashed password
    """
    if isinstance(password, str):
        password = password.encode('utf-8')
    
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)

def verify_password(password: Union[str, bytes], hashed: Union[str, bytes]) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password: The password to verify (can be string or bytes)
        hashed: The hashed password to check against (can be string or bytes)
        
    Returns:
        bool: True if the password matches, False otherwise
    """
    if isinstance(password, str):
        password = password.encode('utf-8')
    if isinstance(hashed, str):
        hashed = hashed.encode('utf-8')
    
    return bcrypt.checkpw(password, hashed) 