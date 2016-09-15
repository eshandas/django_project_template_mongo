from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings.local')

app = Celery('main',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',
             include=['utils.email_tasks'])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))

CELERY_TIMEZONE = 'UTC'
