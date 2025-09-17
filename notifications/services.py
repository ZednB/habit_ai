from datetime import datetime

from sqlalchemy.orm import Session

from notifications import models, schemas


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
