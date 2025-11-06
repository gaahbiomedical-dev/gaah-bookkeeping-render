from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "your-secret-key"  # replace with your actual secret key
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Maximum bcrypt password length
BCRYPT_MAX_LENGTH = 72

def get_password_hash(password: str) -> str:
    # Truncate password to 72 bytes if needed
    truncated = password[:BCRYPT_MAX_LENGTH]
    return pwd_context.hash(truncated)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    truncated = plain_password[:BCRYPT_MAX_LENGTH]
    return pwd_context.verify(truncated, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
<<<<<<< HEAD
    return encoded_jwt
=======
    return encoded_jwt
>>>>>>> 1c071df926c702b72a64ef539685c19e319a01de
