from django.core.management import BaseCommand

from users.models import Users


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = Users.objects.create(email='1st.trillionaire.dm@gmail.com')
        user.set_password('zxcdfrt56')
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
