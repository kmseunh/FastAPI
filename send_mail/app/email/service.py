from fastapi import HTTPException
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from app.config import settings

conn_config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_USE_TLS,
    MAIL_SSL_TLS=settings.MAIL_USE_SSL,
)

fast_mail = FastMail(conn_config)


async def send_email(email_data: dict):
    try:
        message = MessageSchema(
            subject=email_data["subject"],
            recipients=email_data["recipients"],
            body=email_data["body"],
            subtype="html",
        )
        await fast_mail.send_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
