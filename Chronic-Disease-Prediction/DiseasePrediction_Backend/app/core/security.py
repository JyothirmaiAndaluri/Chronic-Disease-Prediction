from passlib.context import CryptContext
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ FIXED
def hash_password(password: str):
    return pwd_context.hash(password[:72])

# ✅ FIXED
def verify_password(plain, hashed):
    return pwd_context.verify(plain[:72], hashed)

def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None