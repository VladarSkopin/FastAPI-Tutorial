# Security Helper Functions

from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Any

from config import ALGORITHM, SECRET_KEY
from schemas import TokenData


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
)


def verify_pwd(plain_pwd: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_pwd, hashed_password)  # if they match -> success


def get_pwd_hash(pwd: str) -> str:
    return pwd_context.hash(pwd)  # will return a bunch of gibberish


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
		
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Could not verify credentials", 
                headers={"WWW-Authenticate":"Bearer"})
        return TokenData(email=email)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Could not verify credentials", 
                            headers={"WWW-Authenticate":"Bearer"})
    