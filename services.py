import bcrypt


def make_password(password: str) -> str:
    """Hashes a password and returns the hash as a string."""
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash.decode()


def check_password(password: str, hash_str: str) -> bool:
    """Checks if a password matches the stored hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hash_str.encode('utf-8'))