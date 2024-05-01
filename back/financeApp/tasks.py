from __future__ import absolute_import, unicode_literals
from celery import shared_task
from financeMain.celery import app
import time
from django.core.mail import send_mail
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import datetime


channel_layer = get_channel_layer()

@app.task(bind=True)
def loop_task(self, l):
    for i in range(int(l)):
        print(i)
        time.sleep(1)
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': l})
    print('Task completed')
    async_to_sync(channel_layer.group_send)('info', {"type": "send_info",
                                                    'data': l,
                                                    'operation': 'Long task',
                                                     'datetime': datetime.datetime.now().strftime('%Y-%m-%d   %H:%M:%S'),
                                                     'status': 'Success'})
    return {'current': 100, 'total': 100, }


@shared_task
def send_email_task(email, message):
    subject = 'FinanceApp'

    time.sleep(5)
    async_to_sync(channel_layer.group_send)('info', {"type": "send_info",
                                                     'data': email,
                                                     'operation': 'Email task',
                                                     'datetime': datetime.datetime.now().strftime('%Y-%m-%d   %H:%M:%S'),
                                                     'status': 'Success'})
    return send_mail(
        subject,
        message,
        '',
        [email],
        fail_silently=False
    )

