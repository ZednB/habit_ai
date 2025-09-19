import os
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv('REDIS_URL')

celery_app = Celery(
    'habit_ai',
    broker=REDIS_URL,
    backend=REDIS_URL
)

from notifications import tasks

celery_app.conf.task_routes = {
    'notifications.tasks': {'queue': 'notifications'}
}

celery_app.conf.beat_schedule = {
    'check-notifications-every-minute': {
        'task': 'notifications.tasks.check_notifications',
        'schedule': crontab(minute='*')
    },
}
