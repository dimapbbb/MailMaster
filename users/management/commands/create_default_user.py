from django.core.management import BaseCommand

from users.models import Users


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = Users.objects.create(email='default@gmail.com')
        user.set_password('default_user')
        user.id = 1
        user.username = "default"
        user.is_active = False
        user.is_staff = True
        user.is_superuser = True
        user.save()
