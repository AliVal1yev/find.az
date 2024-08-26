from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings


@shared_task
def send_order_conf_mail_task(email):
    send_mail(
        'Order Confirmation',
        'Your order has been completed',
        'eliveliyev150@gmail.com',
        [email],
        fail_silently=False,
    )

