import smtplib
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from config import settings
from newsletterapp.models import NewsletterSettings, Newsletter, NewsletterLogs
from recepients.models import Client


def start():
    """ Запуск фонового планировщика, чекает базу раз в минуту"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_db, 'interval', seconds=60)
    scheduler.start()


def check_db():
    """ Проверка базы рассылок на необходимость отправки """
    current_date = datetime.now()
    newsletters = NewsletterSettings.objects.filter(next_send_day=current_date.date()).filter(status=True)
    for newsletter in newsletters:
        if str(newsletter.send_time)[:5] == str(current_date.time())[:5]:

            send_newsletter(newsletter.newsletter_id, send_method="По расписанию")


def send_newsletter(newsletter_id, send_method):
    """
    Отправляет рассылку
    """
    send_mails(**newsletter_form(newsletter_id, send_method))
    update_newsletter(NewsletterSettings.objects.get(newsletter=newsletter_id))


def send_mails(email_list, newsletter, log_data):
    """ Отправляет письмa списку получателей"""
    try:
        send_mail(
            newsletter.topic,
            newsletter.content,
            settings.EMAIL_HOST_USER,
            email_list,
            fail_silently=False
        )
        log_data["status"] = True
        NewsletterLogs.objects.create(**log_data)

    except smtplib.SMTPException as fail:
        log_data["status"] = False
        log_data["server_answer"] = str(fail)
        NewsletterLogs.objects.create(**log_data)


def update_newsletter(newsletter):
    """ Обновление дат следующей и последней попытки"""
    newsletter.last_send_date = datetime.now().date()
    if newsletter.periodicity:
        newsletter.next_send_day += timedelta(days=newsletter.periodicity)
    else:
        newsletter.next_send_day = None
        newsletter.status = False
    newsletter.save()


def newsletter_form(newsletter_id, send_method="По расписанию"):
    """
    Формирование параметров для рассылки
    """
    newsletter = Newsletter.objects.get(pk=newsletter_id)
    email_list = [recipient.email for recipient in Client.objects.all()]
    log_data = {"newsletter": newsletter,
                "send_method": send_method}
    return {
        "newsletter": newsletter,
        "email_list": email_list,
        "log_data": log_data
    }
