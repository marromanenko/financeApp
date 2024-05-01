from __future__ import absolute_import, unicode_literals
from celery import Celery
from kombu import Exchange, Queue

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'financeMain.settings')

default_queue_name = 'celery'
default_exchange_name = 'celery'
default_routing_key = 'celery'

firstqueue_queue_name = 'firstqueue'
firstqueue_routing_key = 'firstqueue'

secondqueue_queue_name = 'secondqueue'
secondqueue_routing_key = 'secondqueue'

app = Celery('financeMain', backend='rpc://', broker='amqp://')

default_exchange = Exchange(default_exchange_name, type='direct')
default_queue = Queue(
    default_queue_name,
    default_exchange,
    routing_key=default_routing_key)

firstqueue_queue = Queue(
    firstqueue_queue_name,
    default_exchange,
    routing_key=firstqueue_routing_key)

secondqueue_queue = Queue(
    secondqueue_queue_name,
    default_exchange,
    routing_key=secondqueue_queue_name)

app.conf.task_queues = (default_queue, firstqueue_queue, secondqueue_queue)

app.conf.task_default_queue = default_queue_name
app.conf.task_default_exchange = default_exchange_name
app.conf.task_default_routing_key = default_routing_key

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
