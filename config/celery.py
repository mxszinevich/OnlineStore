import os

from celery import Celery
from celery.schedules import crontab

from config import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.task_default_queue = 'garbage_remove'

app.conf.task_routes = {'products.tasks.check_discounts_products': {'queue': 'discounts'}}

app.conf.beat_schedule = {
    'celery_check_discounts_products': {
        'task': 'products.tasks.check_discounts_products',
        'schedule': crontab(minute='*/2')
    },
    'celery_delete_user_carts': {
        'task': 'products.tasks.delete_user_carts',
        'schedule': crontab(minute='*/1')
    }
}
app.conf.timezone = settings.TIME_ZONE
