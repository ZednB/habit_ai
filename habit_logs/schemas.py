from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HabitLogBase(BaseModel):
    note: str = ''


class HabitLogCreate(HabitLogBase):
    pass


class HabitLogUpdate(BaseModel):
    note: Optional[str] = None


class HabitLogOut(HabitLogBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
