from django.core.mail import send_mail
from config.celery import app


@app.task
def send_order_confirm(email, post_id):
    send_mail(
        'Order confirm',
        f'http://localhost:8000/api/v1/car/{post_id}/order_confirm/',
        'rafievvvv@gmail.com',
        [email]
    )