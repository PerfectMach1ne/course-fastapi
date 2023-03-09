from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status

from . import schemas, models
from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')  # from auth.py "login" name in the path decorator

# SECRET_KEY from command openssl
# The algorithm
# The token expiration date
# Run this in git or bash: openssl rand -hex 32
SECRET_KEY = "7580d10d73efcfc5f0ef56df5db0ebc3ccbd59b8a6461f5ed0d78b73e0c1558d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120


def create_access_token(data: dict):
    to_encode = data.copy()

    # Important: utcnow(), not now()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        # Decode the JWT token into a payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Extract the id from the payload
        id: str = payload.get("user_id")

        # If there's no id, throw an error
        if id is None:
            raise credentials_exception

        # Validate /w the schema the token data
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials.",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
