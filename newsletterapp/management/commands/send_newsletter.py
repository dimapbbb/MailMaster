from django.core.management import BaseCommand

from newsletterapp.utils import send_newsletter


class Command(BaseCommand):

    def handle(self, newsletter_id, *args, **options):
        send_newsletter(newsletter_id)
