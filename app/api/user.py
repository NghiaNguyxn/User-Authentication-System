from fastapi import APIRouter, BackgroundTasks

from app import crud, models, email, dependencies
from app.dependencies import SessionDep
from app.config import settings

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/me", response_model=models.UserResponse)
async def read_user_me(
    current_user: dependencies.CurrentUser
):
    """Retrieve current user infomation"""

    return current_user

@router.patch("/me", response_model=models.UserResponse)
async def update_user_me(
    user_update: models.UserUpdate,
    current_user: dependencies.CurrentUser,
    session: SessionDep
):
    """Update user information"""

    update_user = crud.update_user(session, current_user.id, user_update)

    return update_user

@router.post("/change-password")
async def change_password(
    request: models.ChangePasswordRequest,
    current_user: dependencies.CurrentUser,
    session: SessionDep
):
    """Change password"""

    user = crud.change_password(session, current_user.id, request.current_password, request.new_password)

    return {"message": "Paswword changed successfully"}

@router.post("/resend-verification")
async def resend_verification(
    current_user: dependencies.CurrentUser,
    session: SessionDep,
    bg_task: BackgroundTasks
):
    """Resend verification email"""

    new_token = crud.regenerate_verification_token(session, current_user)

    bg_task.add_task(email.send_verification_email, current_user, new_token)

    return {"message": "Verification email sent"}