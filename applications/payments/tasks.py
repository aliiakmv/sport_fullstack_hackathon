from django.core.mail import send_mail

from config.celery import app


@app.task
def send_subscription_key_email(email, money, subscription_key):
    full_msg = f'Thank you for buying a subscription. {money} has been withdrawn from your account. ' \
               f'Yout key: {subscription_key}'
    send_mail(
        'Get a subscription key',
        full_msg,
        'aliyakomanovaa@gmail.com',
        [email],
    )
