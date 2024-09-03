from django.core.management import BaseCommand
from django.core.mail import send_mail

from config import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        send_mail(
            "Subject here",
            "Here is the message.",
            settings.EMAIL_HOST_USER,
            ["1st.trillionaire.dm@gmail.com"],
        )
