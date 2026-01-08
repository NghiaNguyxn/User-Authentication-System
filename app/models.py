from datetime import datetime
from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel, Field, func

# BASE MODELS
class UserBase(SQLModel):
    username: str = Field(unique=True, index=True, nullable=False)
    email: EmailStr = Field(unique=True, index=True, nullable=False)
    full_name: str | None = Field(default=None)

# TABLE MODELS
class UserDB(UserBase, table=True):
    __tablename__: str = "users"

    id: int | None = Field(default=None, primary_key=True, index=True)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    verification_token: str | None = Field(default=None)
    reset_token: str | None = Field(default=None)
    reset_token_expires: datetime | None = Field(default=None)

    # Sử dụng sa_column để dùng các tính năng đặc biệt của SQLAlchemy
    created_at: datetime = Field(
        default=None,
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        default=None,
        sa_column_kwargs={
            "onupdate": func.now(),
            "server_default": func.now()
        }
    )

# ACTION SCHEMAS (Cho request/response)
class UserCreate(UserBase):
    password: str = Field(min_length=8)
    password_confirm: str

    @field_validator("password_confirm")
    def passwords_match(cls, v, info):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Password do not match")
        return v
    
class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime

class UserUpdate(SQLModel): # Không kế thừa Base vì các trường này đều là Optional
    username: str | None = None
    email: EmailStr | None = None
    full_name: str | None = None

class Token(SQLModel):
    access_token: str
    token_type: str
    message: str | None = None

class TokenData(SQLModel):
    username: str | None = None

class ChangePasswordRequest(SQLModel):
    current_password: str
    new_password: str = Field(min_length=8)
    confirm_password: str

    @field_validator("confirm_password")
    def passwords_match(cls, v, info):
        if "new_password" in info.data and v != info.data["new_password"]:
            raise ValueError("Password do not match")
        return v

class ResetPasswordRequest(SQLModel):
    token: str
    new_password: str = Field(min_length=8)
    confirm_password: str

    @field_validator("confirm_password")
    def passwords_match(cls, v, info):
        if "new_password" in info.data and v != info.data["new_password"]:
            raise ValueError("Password do not match")
        return v