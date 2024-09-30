from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    photo = models.ImageField(upload_to="users_photo/", verbose_name="фотография", blank=True, null=True)
    phone = models.IntegerField(verbose_name="Номер телефона", blank=True, null=True)
    country = models.CharField(max_length=50, verbose_name="Страна", blank=True, null=True)

    def __str__(self):
        return f"{self.username}"

    def is_manager(self):
        if self.groups.filter(name="newsletter_manager").exists():
            return True
        return False

    def is_content_manager(self):
        if self.groups.filter(name="content_manager").exists():
            return True
        return False

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

        permissions = [
            ('can_view_users', 'view users list'),
            ('can_block_user', 'block or unblock user'),
        ]
