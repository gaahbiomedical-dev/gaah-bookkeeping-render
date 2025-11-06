from passlib.context import CryptContext

# Configure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hash the password using bcrypt.
    Truncate to 72 characters to avoid bcrypt limitation.
    """
    truncated = password[:72]  # Bcrypt max length
    return pwd_context.hash(truncated)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    """
    truncated = plain_password[:72]  # ensure consistency
    return pwd_context.verify(truncated, hashed_password)
