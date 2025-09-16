from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import status

from habits import models, schemas


def get_habits(db: Session, user_id: int):
    return db.query(models.Habit).filter(models.Habit.owner_id == user_id).all()


def get_habit(db: Session, habit_id: int, user_id: int):
    return db.query(models.Habit).filter(
        models.Habit.id == habit_id,
        models.Habit.owner_id == user_id
    ).first()


def create_habit(db: Session, habit: schemas.HabitCreate, user_id):
    db_habit = models.Habit(**habit.dict(), owner_id=user_id)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit


def update_habit(db: Session, habit_id: int, habit_update: schemas.HabitUpdate, user_id: int):
    db_habit = db.query(models.Habit).filter(
        models.Habit.id == habit_id,
        models.Habit.owner_id == user_id
    ).first()
    if not db_habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такой привычки не найдено'
        )
    update_data = habit_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_habit, key, value)
    db.commit()
    db.refresh(db_habit)
    return db_habit


def delete_habit(db: Session, habit_id: int, user_id: int):
    habit = get_habit(db, habit_id, user_id)
    if habit:
        db.delete(habit)
        db.commit()
    return habit
