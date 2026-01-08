from typing import Annotated
from datetime import timedelta
import logging
from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm

from app import crud, models, email, security
from app.dependencies import SessionDep
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", 
          response_model=models.UserResponse, 
          status_code=status.HTTP_201_CREATED)
async def register(
    user: models.UserCreate,
    session: SessionDep,
    bg_tasks: BackgroundTasks
):
    """Register a new account"""
    
    new_user = crud.create_user(session, user)
    
    bg_tasks.add_task(email.send_verification_email, new_user, new_user.verification_token)
    
    return new_user

@router.post("/login", response_model=models.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
) -> models.Token:
    """Log in and receive JWT tokens"""

    # Authenticate user
    user = crud.authenticate_user(session, form_data.username, form_data.password)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return models.Token(access_token=access_token, token_type="bearer")

@router.get("/verify-email")
async def verify_email(
    token: str,
    session: SessionDep
):
    """Email verification and login"""

    user = crud.verify_email_token(session, token)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return models.Token(
        access_token=access_token,
        token_type="bearer",
        message="Email verified and logged in successfully!"
    )

@router.post("/forgot-password")
async def forgot_password(
    user_email: str,
    session: SessionDep,
    bg_task: BackgroundTasks
):
    """Send a password reset email"""

    try:
        reset_token = crud.create_password_reset_token(session, user_email)
        user = crud.get_user_by_email(session, user_email)
        bg_task.add_task(email.send_password_reset_email, user, reset_token)
    except Exception as e:
        logger.error(f"Error sending password reset email: {e}")
    
    return {
        "message": "If your email is registered, you will receive a password reset link"
    }

@router.post("/reset-password")
async def reset_password(
    request: models.ResetPasswordRequest,
    session: SessionDep
):
    """Reset password with token and login"""

    user = crud.reset_password(session, request.token, request.new_password)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return models.Token(
        access_token=access_token,
        token_type="bearer",
        message="Password reset successfully. You are now logged in"
    )