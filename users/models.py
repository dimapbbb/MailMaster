from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    photo = models.ImageField(upload_to="users_photo", verbose_name="фотография", blank=True, null=True)

    def __str__(self):
        return f"{self.username}, {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""
