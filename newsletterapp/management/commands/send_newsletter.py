from django.core.management import BaseCommand

from newsletterapp.utils import send_newsletter


class Command(BaseCommand):

    def handle(self, newsletter_id, *args, **options):
        send_newsletter(newsletter_id, send_method="Консоль")

    def add_arguments(self, parser):
        parser.add_argument('newsletter_id', type=int, help='Персональный ключ рассылки')
