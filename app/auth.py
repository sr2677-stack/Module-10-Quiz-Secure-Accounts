from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    # ✅ Truncate to 72 bytes - bcrypt hard limit
    plain_password = plain_password[:72]
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # ✅ Truncate here too for consistency
    plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)