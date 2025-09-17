from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session
from habit_logs import models as log_models, schemas
from habits import models


def get_habit_logs(db: Session, habit_id: int, user_id: int):
    return db.query(log_models.HabitLog).join(models.Habit).filter(
        models.Habit.id == habit_id,
        models.Habit.owner_id == user_id
    ).all()


def get_habit_log(db: Session, log_id, user_id):
    return (
        db.query(log_models.HabitLog)
        .join(models.Habit)
        .filter(and_(log_models.HabitLog.id == log_id,
                models.Habit.owner_id == user_id))
        .first()
    )


def create_habit_log(db: Session, log: schemas.HabitLogCreate, habit_id: int, user_id: int):
    habit = db.query(models.Habit).filter(
        models.Habit.id == habit_id,
        models.Habit.owner_id == user_id
    ).first()
    if not habit:
        return None

    db_log = log_models.HabitLog(**log.dict(), habit_id=habit_id)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def update_habit_log(db: Session, log_id: int, log: schemas.HabitLogUpdate, user_id: int):
    db_log = (
        db.query(log_models.HabitLog)
        .join(models.Habit)
        .filter(
            log_models.HabitLog.id == log_id,
            models.Habit.owner_id == user_id
        ).first()
    )
    if not db_log:
        return None
    db_log.note = log.note
    db.commit()
    db.refresh(db_log)
    return db_log


def delete_habit_log(db: Session, log_id: int, user_id: int):
    db_log = db.query(log_models.HabitLog).join(models.Habit).filter(
        log_models.HabitLog.id == log_id,
        models.Habit.owner_id == user_id
    ).first()
    if not db_log:
        return None
    db.delete(db_log)
    db.commit()
    return db_log


def toggle_habit_log_status(db: Session, log_id: int, user_id: int):
    db_log = (db.query(log_models.HabitLog)
              .join(models.Habit)
              .filter(log_models.HabitLog.id == log_id,
                      models.Habit.owner_id == user_id)
              ).first()
    if not db_log:
        return None
    db_log.status = 'done' if db_log.status == 'not_done' else 'not_done'
    db_log.completed_at = datetime.now() if db_log.status == 'done' else datetime.now()
    db.commit()
    db.refresh(db_log)
    return db_log
