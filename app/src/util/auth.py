# app/src/util/auth.py
import os
import logging
from datetime import datetime, timedelta

from jose import JWTError, jwt
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.src.models.user import User

# Load environment variables from .env
load_dotenv()

# Config
SECRET_KEY = os.getenv("SECRET_KEY", "EmqUQGgxtxATSKl299MYnliwM99Iu6zj4v56HShpIT4RAXXAfQ31ce8r/I388KzGJuUkc0+JTBQe7EULO30Qtg==")
if SECRET_KEY == "EmqUQGgxtxATSKl299MYnliwM99Iu6zj4v56HShpIT4RAXXAfQ31ce8r/I388KzGJuUkc0+JTBQe7EULO30Qtg==":
    logging.warning("!! USING DEFAULT SECRET KEY !!\n You NEED to give a different secret key as an environmental variable!")
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 
REFRESH_TOKEN_EXPIRE_DAYS = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")  # Your login URL

# Password hashing
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# Token creation
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

# Token verification
def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    from app.src.util.db import get_db  # avoid circular import
    from sqlalchemy.future import select
    import asyncio

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Look up the user from DB synchronously
    db = asyncio.run(get_db().__anext__())
    result = db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user
