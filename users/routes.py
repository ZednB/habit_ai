from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from core import security
from core.database import get_db
from users import schemas, services, models

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/', response_model=List[schemas.UserOut])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = services.get_users(db, skip=skip, limit=limit)
    return users


@router.get('/{user_id}', response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = services.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return db_user


@router.get('/me', response_model=schemas.UserOut)
def read_current_user(current_user: models.User = Depends(security.get_current_user)):
    return current_user


@router.post('/register', response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail='Пользователь уже зарегистрирован'
        )
    new_user = services.create_user(db, user)
    return new_user


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = services.authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неправильная почта или пароль',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token = security.create_access_token({'user_id': user.id})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.delete('/me', response_model=schemas.UserOut)
def delete_current_user(current_user: models.User = Depends(security.get_current_user),
                        db: Session = Depends(get_db)):
    services.delete_user(db, current_user)
    return current_user


@router.post('/link-telegram')
def link_telegram(email: str, chat_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == email
    ).first()
    if not user:
        return {'error': 'Пользователь не найден'}
    user.telegram_chat_id = chat_id
    db.commit()
    db.refresh(user)
    return {'message': 'Телеграм успешно привязан'}
