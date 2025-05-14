from celery import Celery
from celery.schedules import crontab
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NoticeBoard.settings')

app = Celery('NoticeBoard')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_five_minutes': {
        'task': 'boardapp.tasks.delete_confirmation_code',
        'schedule': 300,
    },
    'action_every_week': {
        'task': 'boardapp.tasks.weekly_news',
        'schedule': crontab(minute=0, hour=10, day_of_week='sunday'),
    },
}
