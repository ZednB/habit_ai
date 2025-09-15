from fastapi import APIRouter, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from starlette import status

from core.database import get_db
from users import services, schemas

templates = Jinja2Templates(directory='templates')

router = APIRouter(
    prefix='/web/users',
    tags=['users-web']
)


@router.get('/')
def users_list(request: Request, db: Session = Depends(get_db)):
    users = services.get_users(db)
    return templates.TemplateResponse('index.html', {'request': request, 'users': users})


@router.get('/register')
def register_form(request: Request):
    return templates.TemplateResponse('users/register.html', {'request': request})


@router.post('/register')
def register_user(
        # request: Request,
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    user_data = schemas.UserCreate(username=username, email=email, password=password)
    services.create_user(db, *user_data)
    return RedirectResponse(url='/web/users', status_code=status.HTTP_303_SEE_OTHER)


@router.get('/login')
def login_user(request: Request,
               email: str = Form(...),
               password: str = Form(...),
               db: Session = Depends(get_db)):
    user = services.authenticate_user(db, email, password)
    if not user:
        return templates.TemplateResponse('users/login.html',
                                          {'request': request,
                                           'error': 'Неправильная почта или пароль'})
    return RedirectResponse(url=f"/web/users/{user.id}", status_code=status.HTTP_303_SEE_OTHER)


@router.get('/{user_id}')
def user_profile(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = services.get_user_by_id(db, user_id)
    if not user:
        return RedirectResponse(url='/web/users', status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse('users/profile.html', {'request': request, 'user': user})
