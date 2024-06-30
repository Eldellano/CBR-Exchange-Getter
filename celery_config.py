from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv
import os

load_dotenv()

app = Celery('celery_config', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
import tasks

check_time = os.getenv('CHECK_TIME')
check_hour, check_minute = check_time.split(':')

app.conf.beat_schedule = {
    'run_exchange_get-every-day': {
        'task': 'tasks.run_exchange_get',
        'schedule': crontab(hour=str(check_hour), minute=str(check_minute)),
    },
}

app.conf.timezone = 'Europe/Moscow'
