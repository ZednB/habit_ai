from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user
from habits import schemas, services

router = APIRouter(
    prefix='/habits',
    tags=['habits']
)


@router.post('/create', response_model=schemas.HabitOut, status_code=status.HTTP_201_CREATED)
def create_habit(
        habit: schemas.HabitCreate,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    return services.create_habit(db, habit, user.id)


@router.put('/update/{habit_id}', response_model=schemas.HabitOut)
def update_habit(
        habit_id: int,
        habit: schemas.HabitUpdate,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    return services.update_habit(db, habit_id, habit, user.id)


@router.get('/', response_model=List[schemas.HabitOut])
def get_habits(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return services.get_habits(db, user.id)


@router.get('/{habit_id}', response_model=schemas.HabitOut)
def get_habit(habit_id: int,
              db: Session = Depends(get_db),
              user=Depends(get_current_user)):
    habit = services.get_habit(db, habit_id, user.id)
    if not habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такой привычки не найдено')
    return habit


@router.delete('/delete/{habit_id}', response_model=schemas.HabitOut)
def delete_habit(habit_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    habit = services.delete_habit(db, habit_id, user.id)
    if not habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такой привычки не найдено')
    return habit
