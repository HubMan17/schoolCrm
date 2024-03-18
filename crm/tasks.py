from backend.celery import app
from celery import shared_task
from django.core.mail import send_mail
import time


@shared_task
def send_mail_to_enrollee(lastName, firstName, email, password, enrolleeProfile):
    
    # send login and password to email
    text = f"""Здравствуйте, {lastName} {firstName}, Ваше заявление было успешно принято.

Для получения дальнейшей информации вы можете обратиться в отдел приёмной комиссии КЭСП или использовать данные для авторизации в вашем профиле на сайте учебной организации:
Ваш логин: {email}
Ваш пароль: {password}"""

    return send_mail('Приёмная комиссия КЭСП', text, 
                    'notification@dzhanatly.fvds.ru', [enrolleeProfile], fail_silently=False)
