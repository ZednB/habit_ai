from pydantic import EmailStr

from core.celery_app import celery_app
from core.database import SessionLocal
from core.email import send_email_notification
from core.telegram import send_telegram_notification
from notifications import services


@celery_app.task
def send_email_task(email: str, subject: str, body: str):
    import asyncio
    asyncio.run(send_email_notification(email, subject, body))


@celery_app.task
def send_telegram_task(chat_id: int, text: str):
    import asyncio
    asyncio.run(send_telegram_notification(chat_id, text))


@celery_app.task
def check_notifications():
    print('[DEBUG check_notfications вызвана')
    db = SessionLocal()
    try:
        services.process_notifications(db)
    finally:
        db.close()
