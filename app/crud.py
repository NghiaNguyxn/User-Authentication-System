from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select, or_
from sqlalchemy.exc import IntegrityError

from app import models, exceptions, security

# User READ operations
def get_user(session: Session, user_id: int):
    """Find user by user id"""

    return session.get(models.UserDB, user_id)

def get_user_by_email(session: Session, email: str):
    """Find user by email"""

    statement = select(models.UserDB).where(models.UserDB.email == email)
    return session.exec(statement).first()

def get_user_by_username(session: Session, username: str):
    """Find user by username"""

    statement = select(models.UserDB).where(models.UserDB.username == username)
    return session.exec(statement).first()

def get_user_by_username_or_email(session: Session, username_or_email: str):
    """Find user by username or email"""
    
    statement = select(models.UserDB).where(
        or_(
            models.UserDB.username == username_or_email,
            models.UserDB.email == username_or_email
        )
    )
    return session.exec(statement).first()

def get_users(session: Session, skip: int = 0, limit: int = 100) -> list[models.UserDB]:
    statement = select(models.UserDB).offset(skip).limit(limit)
    return session.exec(statement).all()

# User WRITE operations
def create_user(session: Session, user_create: models.UserCreate):
    """Create a new user"""
    
    # Check exists
    if get_user_by_username(session, user_create.username):
        raise exceptions.UserAlreadyExists("Username already taken")
    
    if get_user_by_email(session, user_create.email):
        raise exceptions.UserAlreadyExists("Email already registered")
    
    # Create hash password and token
    hashed_pw = security.get_password_hash(user_create.password)
    v_token = security.create_verification_token()

    # Convert from schema to model database
    db_user = models.UserDB.model_validate(
        user_create,
        update={"hashed_password": hashed_pw, "verification_token": v_token}
    )

    session.add(db_user)
    
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise exceptions.UserAlreadyExists("Email or username has been compromised")

    session.refresh(db_user)
    return db_user

def update_user(session: Session, user_id: int, user_update: models.UserUpdate):
    """Update user information"""
    
    db_user = get_user(session, user_id)
    if not db_user:
        raise exceptions.UserNotFound()
    
    update_data = user_update.model_dump(exclude_unset=True)

    if "email" in update_data and update_data["email"] != db_user.email:
        if get_user_by_email(session, update_data["email"]):
            raise exceptions.UserAlreadyExists("Email already registered")
        
    if "username" in update_data and update_data["username"] != db_user.username:
        if get_user_by_username(session, update_data["username"]):
            raise exceptions.UserAlreadyExists("Username already taken")
    
    db_user.sqlmodel_update(update_data)

    session.add(db_user)
    
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise exceptions.UserAlreadyExists("Email or username has been compromised")

    session.refresh(db_user)
    return db_user

def delete_user(session: Session, user_id: int):
    """Delete user"""

    db_user = get_user(session, user_id)
    if not db_user:
        raise exceptions.UserNotFound()
    
    session.delete(db_user)
    session.commit()
    return True

# Auth and Token operations
def authenticate_user(session: Session, username: str, password: str):
    """User authentication"""
    
    user: models.UserDB = get_user_by_username_or_email(session, username)
    if not user or not security.verify_password(password, user.hashed_password):
        raise exceptions.IncorrectCredentials()
    
    if not user.is_active:
        raise exceptions.UserInactive()

    return user

def verify_email_token(session: Session, token: str):
    """Verify email using a token"""

    statement = select(models.UserDB).where(models.UserDB.verification_token == token)
    user = session.exec(statement).first()

    if not user:
        raise exceptions.UserNotFound()
    
    if user.is_verified:
        raise exceptions.UserAlreadyVerified()

    user.is_verified = True
    user.verification_token = None
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def regenerate_verification_token(session: Session, user: models.UserDB):
    """Regenerate verification token"""

    if user.is_verified:
        raise exceptions.UserAlreadyVerified()
    
    user.verification_token = security.create_verification_token()
    session.add(user)
    session.commit()
    session.refresh(user)
    return user.verification_token

def create_password_reset_token(session: Session, email: str):
    """Create a password reset token"""

    user: models.UserDB = get_user_by_email(session, email)
    if not user:
        raise exceptions.UserNotFound()
    
    user.reset_token = security.create_reset_token()
    user.reset_token_expires = datetime.now(timezone.utc) + timedelta(hours=24)

    session.add(user)
    session.commit()
    return user.reset_token
    
def reset_password(session: Session, token: str, new_password: str):
    """Reset password using token"""

    now = datetime.now(timezone.utc)
    statement = select(models.UserDB).where(
        models.UserDB.reset_token == token,
        models.UserDB.reset_token_expires > now
    )
    user = session.exec(statement).first()

    if not user:
        raise exceptions.InvalidToken()
    
    if security.verify_password(new_password, user.hashed_password):
        raise exceptions.PasswordSameAsOld()
    
    user.hashed_password = security.get_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expires = None

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def change_password(session: Session, user_id: int, current_password: str, new_password: str):
    """Change your password when you know the old password"""

    user: models.UserDB = get_user(session, user_id)
    if not user:
        raise exceptions.UserNotFound()
    
    if not security.verify_password(current_password, user.hashed_password):
        raise exceptions.IncorrectCredentials()
    
    user.hashed_password = security.get_password_hash(new_password)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user