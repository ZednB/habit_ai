from typing import Optional
from pydantic import BaseModel


class HabitBase(BaseModel):
    name: str
    frequency: str
    status: Optional[str] = 'not_done'


class HabitCreate(HabitBase):
    pass


class HabitUpdate(BaseModel):
    name: Optional[str]
    frequency: Optional[str]
    status: Optional[str]


class HabitOut(HabitBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
