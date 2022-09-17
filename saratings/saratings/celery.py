import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saratings.settings")

#Works with broker url set in settings.py
app = Celery("saratings")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Africa/Johannesburg'

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

"""
If error below:
kombu.exceptions.OperationalError: [Errno 61] Connection refused

Add these lines to the __init__.py of the project
from __future__ import absolute_import
from .celery import app as celery_app


__all__ = ('celery_app',)

"""