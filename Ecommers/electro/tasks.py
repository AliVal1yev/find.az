from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings


@shared_task
def send_order_conf_mail_task():
    send_mail(
        'Order Confirmation',
        'Your order has been completed',
        'eliveliyev150@gmail.com',
        ['alivaliyev150@gmail.com'],
        fail_silently=False,
    )


@shared_task()
def send_login_mail_task():
    send_mail(
        subject='Order Confirmation',
        message='Your order has been completed successfully.',
        from_email='eliveliyev150@gmail.com', 
        recipient_list=['alivaliyev150@gmail.com'],
        fail_silently=False,
    )