from datetime import datetime
import enum

from sqlalchemy import Column, Integer, ForeignKey, Time, Enum, String, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class NotificationEnum(str, enum.Enum):
    email = 'email'
    telegram = 'telegram'
    push = 'push'


class Notification(Base):
    __tablename__ = 'notification'

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(ForeignKey('habits.id'), nullable=False)
    send_time = Column(Time, nullable=False)
    channel = Column(Enum(NotificationEnum), nullable=False, default=NotificationEnum.email)
    message = Column(String(length=255), nullable=False)
    is_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    habit = relationship('Habit', back_populates='notifications')

    def __repr__(self):
        return f"<Notification(message='{self.message}', habit='{self.habit}')>"

