import os

from fastapi import APIRouter
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import EmailStr

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_FROM'),
    MAIL_PORT=os.getenv('MAIL_PORT'),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_STARTTLS=os.getenv('MAIL_STARTTLS'),
    MAIL_SSL_TLS=os.getenv('MAIL_SSL_TLS'),
    USE_CREDENTIALS=os.getenv('USE_CREDENTIALS'),
)

fm = FastMail(conf)


async def send_email_notification(email: EmailStr, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype='plain'
    )
    await fm.send_message(message)

router = APIRouter()


@router.post('/send-test-email')
async def send_test_email(email: EmailStr):
    subject = 'Тестовое письмо'
    body = 'smtp работает'
    await send_email_notification(email, subject, body)
    return {'status': 'ok', 'message': f'Письмо отправлено на {email}'}
