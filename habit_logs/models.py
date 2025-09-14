import enum
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Date, Enum, String, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class LogStatusEnum(str, enum.Enum):
    done = 'done'
    not_done = 'not_done'


class HabitLog(Base):
    __tablename__ = 'habit_logs'

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(ForeignKey('habits.id'), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum(LogStatusEnum), default=LogStatusEnum.not_done, nullable=False)
    note = Column(String(length=255))
    created_at = Column(DateTime, default=datetime.utcnow)

    habit = relationship('Habit', back_populates='logs')

    def __repr__(self):
        return f"<HabitLog(name='{self.note}', habit='{self.habit}')>"
