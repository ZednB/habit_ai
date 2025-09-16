from typing import Optional
from pydantic import BaseModel


class HabitBase(BaseModel):
    name: str
    frequency: str
    status: Optional[str] = 'not_done'


class HabitCreate(HabitBase):
    pass


class HabitUpdate(BaseModel):
    name: Optional[str] = None
    frequency: Optional[str] = None
    status: Optional[str] = None


class HabitOut(HabitBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
