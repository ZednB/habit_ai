from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from core.database import Base
from habits.models import Habit
from habit_logs.models import HabitLog


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=50), index=True, nullable=False)
    email = Column(String(length=150), index=True, unique=True, nullable=False)
    hashed_password = Column(String(length=255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    habits = relationship('Habit', back_populates='owner')

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
