from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from core.config import settings
from core.database import SessionLocal
from users import models

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')


def hash_password(password: str) -> str:
    """
    Принимает пароль и возвращает хешированный
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Проверяет совпадает ли переданный и захешированный пароль
    """
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создаем JWT токен
    :param data:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Декодирует JWT токен
    Если все ок - возвращает payload (данные внутри токена)
    Иначе None
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get('user_id')
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail='Неправильная аутентификация'
            )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail='Неправильная аутентификация'
        )
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    db.close()
    if user is None:
        raise HTTPException(
            status_code=401,
            detail='Пользователь не найден'
        )
    return user
