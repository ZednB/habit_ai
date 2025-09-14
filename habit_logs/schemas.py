from datetime import datetime

from pydantic import BaseModel


class HabitLogBase(BaseModel):
    habit_id: int
    note: str = ''


class HabitLogCreate(HabitLogBase):
    pass


class HabitLogOut(HabitLogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
