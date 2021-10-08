from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

from django.conf import settings
from kombu import Exchange

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config", broker=settings.CELERY_BROKER_URL)
app.config_from_object("config.settings", namespace="CELERY")

default_exchange = Exchange('manager', type='direct')

app.conf.task_default_queue = 'manager'
app.conf.task_default_exchange = 'manager'
app.conf.task_default_routing_key = 'manager'
app.conf.task_always_eager = True
app.conf.accept_content = ['json']
app.conf.task_serializer = 'json'
app.conf.result_accept_content = ['json']

app.autodiscover_tasks()
