from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import status

from core.database import get_db
from notifications import schemas, services

router = APIRouter(
    prefix='/notifications',
    tags=['notifications']
)


@router.get('/list/{habit_id}', response_model=list[schemas.NotificationOut])
def list_notifications(habit_id: int, db: Session = Depends(get_db)):
    return services.get_notifications(db, habit_id)


@router.get('/{habit_id}/{notification_id}', response_model=schemas.NotificationOut)
def get_notification(habit_id: int, notification_id: int, db: Session = Depends(get_db)):
    notification = services.get_notification(db, notification_id, habit_id)
    if not notification:
        return {'detail': 'Напоминание не найдено'}
    return notification


@router.post('/{habit_id}', response_model=schemas.NotificationOut, status_code=status.HTTP_201_CREATED)
def create_notification(habit_id: int, notification: schemas.NotificationCreate, db: Session = Depends(get_db)):
    notification.habit_id = habit_id
    return services.create_notification(db, notification)


@router.put('/update/{habit_id}/{notification_id}', response_model=schemas.NotificationOut)
def update_notification(habit_id: int,
                        notification_id: int,
                        data: schemas.NotificationUpdate,
                        db: Session = Depends(get_db)):
    notification = services.update_notification(db, notification_id, habit_id, data)
    if not notification:
        return {'detail': 'Напоминание не найдено'}
    return notification



@router.delete('/delete/{habit_id}/{notification_id}', response_model=schemas.NotificationOut)
def delete_notification(habit_id: int, notification_id: int, db: Session = Depends(get_db)):
    notification = services.delete_notification(db, notification_id, habit_id)
    if not notification:
        return {'detail': 'Напоминание не найдено'}
    return notification


@router.post('/sent/{habit_id}/{notification_id}', response_model=schemas.NotificationOut)
def mark_as_sent(habit_id: int, notification_id: int, db: Session = Depends(get_db)):
    notification = services.mark_as_sent(db, notification_id, habit_id)
    if not notification:
        return {'detail': 'Напоминание не найдено'}
    return notification
