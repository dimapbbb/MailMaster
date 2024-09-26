from time import sleep

from django.apps import AppConfig


class NewsletterappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsletterapp'

    def ready(self):
        from newsletterapp.utils import start
        sleep(2)
        start()
