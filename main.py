import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from users.routes import router as user_api_router
from users.web_routes import router as user_web_router
from habits.routes import router as habit_api_router

app = FastAPI()

app.include_router(user_api_router)
app.include_router(user_web_router)
app.include_router(habit_api_router)

templates = Jinja2Templates(directory='templates')

app.mount('/static', StaticFiles(directory='static'), name='static')

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
