from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from core import security
from core.database import get_db
from habit_logs import models, schemas, services
from users import models

router = APIRouter(
    prefix='/habit_logs',
    tags=['habit_logs']
)


@router.post('/create/{habit_id}', response_model=schemas.HabitLogOut, status_code=status.HTTP_201_CREATED)
def create_log(habit_id: int,
               log: schemas.HabitLogCreate,
               db: Session = Depends(get_db),
               current_user: models.User = Depends(security.get_current_user)
               ):
    return services.create_habit_log(db, log, habit_id, current_user.id)


@router.get('/list/{habit_id}/', response_model=List[schemas.HabitLogOut])
def get_logs(habit_id: int,
             db: Session = Depends(get_db),
             current_user: models.User = Depends(security.get_current_user)):
    return services.get_habit_logs(db, habit_id, current_user.id)


@router.get('/{log_id}', response_model=schemas.HabitLogOut)
def get_log(log_id: int,
            db: Session = Depends(get_db),
            user: models.User = Depends(security.get_current_user)):
    db_log = services.get_habit_log(db, log_id=log_id, user_id=user.id)
    if not db_log:
        raise HTTPException(status_code=404, detail='Лог не найден')
    return db_log


@router.put('/update/{log_id}', response_model=schemas.HabitLogOut)
def update_log(log_id: int,
               log: schemas.HabitLogOut,
               db: Session = Depends(get_db),
               current_user: models.User = Depends(security.get_current_user)):
    return services.update_habit_log(db, log_id, log, current_user.id)


@router.delete('/delete/{log_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_log(log_id: int,
               db: Session = Depends(get_db),
               current_user: models.User = Depends(security.get_current_user)):
    services.delete_habit_log(db, log_id, current_user.id)
    return {"detail": "Лог удален"}


@router.put('/status/{log_id}', response_model=schemas.HabitLogOut)
def toggle_status(log_id: int,
                  db: Session = Depends(get_db),
                  current_user: models.User = Depends(security.get_current_user)):
    updated_log = services.toggle_habit_log_status(db, log_id, current_user.id)
    if not updated_log:
        raise HTTPException(status_code=404, detail='Лог не найден')
    return updated_log
