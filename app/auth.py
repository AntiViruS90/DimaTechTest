import os
import bcrypt
import jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv('SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
JWT_EXPIRE_HOURS = os.getenv('JWT_EXPIRE_HOURS')


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_jwt(user_id: int):
    expire = datetime.utcnow() + timedelta(hours=float(JWT_EXPIRE_HOURS))
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
