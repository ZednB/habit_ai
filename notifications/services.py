from datetime import datetime

from sqlalchemy.orm import Session

from notifications import models, schemas

from notifications import tasks


def get_notifications(db: Session, habit_id: int):
    return db.query(models.Notification).filter(
        models.Notification.habit_id == habit_id
    ).order_by(models.Notification.send_time).all()


def get_notification(db: Session, notification_id: int, habit_id: int):
    return db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.habit_id == habit_id
    ).first()


def create_notification(db: Session, notification: schemas.NotificationCreate):
    db_notification = models.Notification(**notification.dict(), created_at=datetime.utcnow())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def update_notification(db: Session, notification_id: int, habit_id: int, data: schemas.NotificationUpdate):
    db_notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.habit_id == habit_id
    ).first()
    if not db_notification:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_notification, key, value)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def delete_notification(db: Session, notification_id: int, habit_id: int):
    db_notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.habit_id == habit_id
    ).first()
    if not db_notification:
        return None
    db.delete(db_notification)
    db.commit()
    return db_notification


def mark_as_sent(db: Session, notification_id: int, habit_id: int):
    db_notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.habit_id == habit_id
    ).first()
    if not db_notification:
        return None
    db_notification.is_sent = not db_notification.is_sent
    db.commit()
    db.refresh(db_notification)
    return db_notification


def process_notifications(db: Session):
    """
    Отправляем уведомления через Celery
    :param db:
    :return:
    """
    now = datetime.now().replace(second=0, microsecond=0).time()
    notifications = db.query(models.Notification).filter(
        models.Notification.send_time <= now,
        models.Notification.is_sent == False
    ).all()
    for notif in notifications:
        habit = notif.habits
        user = habit.owner
        message = f"Напоминание: {habit.name}\n{notif.message}"
        if notif.channel == models.NotificationEnum.email:
            tasks.send_email_task.delay(user.email, 'Напоминание о привычке', message)
        elif notif.channel == models.NotificationEnum.telegram:
            if hasattr(user, 'telegram_id'):
                tasks.send_telegram_task.delay(user.telegram_id, message)
        notif.is_sent = True
        db.commit()
        db.refresh(notif)
