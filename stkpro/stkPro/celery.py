from __future__ import absolute_import, unicode_literals
import os

from django.conf import settings
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stkPro.settings')

app = Celery('stkPro')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'add-every-10-second' : {
        'task' : 'mainapp.tasks.nse_stock_data',
        'schedule' : 10.0,
    },
    # 'add-every-20-second' : {
    #     'task' : 'watch_list_data',
    #     'schedule' : 10,
    # }
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))