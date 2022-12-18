from django.core.mail import send_mail
from config.celery import app


@app.task
def send_confirmation_email(email, code):
    full_link = f'http://localhost:8000/api/v1/account/activate/{code}'
    send_mail(
        'User activation',
        full_link,
        'rafievvvv@gmail.com',
        [email]
    )


@app.task
def send_confirmation_code(email, code):
    send_mail(
        'Password insert',
        f'http://localhost:8000/api/v1/account/forgot_password_complete/ Enter code to link: {code}',
        'rafievvvv@gmail.com',
        [email]
    )