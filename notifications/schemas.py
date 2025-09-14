from datetime import datetime

from pydantic import BaseModel


class NotificationBase(BaseModel):
    user_id: int
    message: str
    is_sent: bool = False


class NotificationCreate(NotificationBase):
    pass


class NotificationOut(NotificationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
