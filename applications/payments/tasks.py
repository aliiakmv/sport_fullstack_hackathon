from django.core.mail import send_mail

from config.celery import app


@app.task
def send_subscription_key_email(email, money, subscription_key):
    full_msg = f'Hello, you have purchased a subscription for the amount of {money} ' \
               f'Follow the link to confir, the payment: http://localhost:8000/api/v1/subscriptions/pay/{subscription_key}'
    send_mail(
        'Get a subscription key',
        full_msg,
        'aliyakomanovaa@gmail.com',
        [email],
    )
