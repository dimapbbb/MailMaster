from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from config import settings
from newsletterapp.models import NewsletterSettings, Newsletter
from recepients.models import Client


def start():
    """ Запуск фонового планировщика, чекает базу раз в минуту"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_db, 'interval', seconds=60)
    scheduler.start()


def check_db():
    """ Проверка базы рассылок на необходимость отправки """
    current_date = datetime.now()
    # Проверка базы на совпадение по дате и времени отправки
    newsletters = NewsletterSettings.objects.filter(next_send_day=current_date.date()).filter(status=True)
    for newsletter in newsletters:
        if str(newsletter.send_time)[:5] == str(current_date.time())[:5]:
            # Формирование сообщения
            mail = Newsletter.objects.get(id=newsletter.newsletter_id)
            # Формирование получателей
            recipients = [recipient.email for recipient in Client.objects.all()]
            # Вызов функции отправки
            send_newsletter(recipients, mail.topic, mail.content)
            # перезаписывание даты след отправки
            newsletter.next_send_day += timedelta(days=newsletter.periodicity)
            newsletter.save()


def send_newsletter(email_list, subject, message):
    """ Отправляет письмо списку получателей"""
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        email_list,
    )
