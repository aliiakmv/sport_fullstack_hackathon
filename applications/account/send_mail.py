from django.core.mail import send_mail
from decouple import config


def send_confirmation_email(email, code):
    full_link = f'http://http://127.0.0.1:8000/api/v1/account/activate/{code}/'
    send_mail(
        'Активация пользователя',
        full_link,
        config('EMAIL_HOST_USER'),
        [email]
    )


def send_confirmation_code(email, code):
    send_mail(
        'Восстановление пароля',
        code,
        config('EMAIL_HOST_USER'),
        [email]
    )
