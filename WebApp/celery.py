import os

from celery import Celery
from django.conf import settings
from kombu import Exchange, Queue, binding

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebApp.settings')

app = Celery('WebApp')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Using a String here means the worker will always find the configuration information
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# Load task modules from all registered Django apps.
app.autodiscover_tasks()

default_exchange = Exchange("default", type='direct')
app.conf.task_default_queue = "default"

app.conf.task_queues = (
    Queue("default", exchange=default_exchange, routing_key="default"),
)

app.conf.task_default_queue = "default"


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
