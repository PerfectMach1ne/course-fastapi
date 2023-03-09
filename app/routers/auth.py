from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schemas, models, utils, oauth2
from ..database import get_db

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)  # might as well be /authentication, whatever you want
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequest Form returns
    # {
    #     "username": "asdf",
    #     "password": "babawa"
    # }
    # It also no longer expects a raw JSON, now it expects form-data

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials.")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials.")

    # Create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # Return a token
    return {"access_token": access_token, "token_type": "bearer"}  # Bearer token
