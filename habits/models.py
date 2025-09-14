import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from core.database import Base


class FrequencyEnum(str, enum.Enum):
    daily = 'daily'
    weekly = 'weekly'
    monthly = 'monthly'


class StatusEnum(str, enum.Enum):
    done = 'done'
    not_done = 'not_done'


class Habit(Base):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50), index=True, nullable=False)
    frequency = Column(Enum(FrequencyEnum), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.not_done, nullable=False)

    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship('User', back_populates='habits')
    log = relationship('HabitLog', back_populates='habits')
    notifications = relationship('Notifications', back_populates='habits')

    def __repr__(self):
        return f"<Habit(name='{self.name}', owner='{self.owner}')>"
