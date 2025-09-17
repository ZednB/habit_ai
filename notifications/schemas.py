from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel

from notifications.models import NotificationEnum


class NotificationBase(BaseModel):
    habit_id: int = None
    send_time: time
    channel: NotificationEnum = NotificationEnum.email
    message: str


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    message: Optional[str] = None
    send_time: Optional[str] = None
    channel: Optional[NotificationEnum] = None
    is_sent: Optional[bool] = None


class NotificationOut(NotificationBase):
    id: int
    is_sent: bool
    created_at: datetime

    class Config:
        orm_mode = True
