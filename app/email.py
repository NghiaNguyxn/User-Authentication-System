from pathlib import Path
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.config import settings
from app.models import UserDB

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,

    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
)

fastmail = FastMail(conf)

async def send_verification_email(user: UserDB, token: str):
    verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"

    message = MessageSchema(
        subject="Account verification",
        recipients=[user.email],
        template_body={
            "username": user.username,
            "url": verify_url
        },
        subtype=MessageType.html
    )

    await fastmail.send_message(message, template_name="verify_email.html")

async def send_password_reset_email(user: UserDB, token: str):
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    message = MessageSchema(
        subject="Recover your password",
        recipients=[user.email],
        template_body={
            "username": user.username,
            "url": reset_url
        },
        subtype=MessageType.html
    )

    await fastmail.send_message(message, template_name="reset_password.html")