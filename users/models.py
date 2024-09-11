from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""
