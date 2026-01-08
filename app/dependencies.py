from typing import Annotated
from sqlmodel import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.database import get_session
from app import crud, models, exceptions, security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SessionDep = Annotated[Session, Depends(get_session)]

async def get_current_user(db : SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = security.verify_token(token)
    if username is None:
        raise credentials_exception
    
    user = crud.get_user_by_username_or_email(db, username)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
        current_user: Annotated[models.UserDB, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise exceptions.UserInactive()
    return current_user

async def get_current_verified_user(
        current_user: Annotated[models.UserDB, Depends(get_current_active_user)]
):
    if not current_user.is_verified:
        raise exceptions.UserNotVerified()
    return current_user

CurrentUser = Annotated[models.UserDB, Depends(get_current_user)]
ActiveUser = Annotated[models.UserDB, Depends(get_current_active_user)]
VerifiedUser = Annotated[models.UserDB, Depends(get_current_verified_user)]