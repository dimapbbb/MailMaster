from django.db import models

from users.models import Users


class Client(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default=3, verbose_name="user")

    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    sur_name = models.CharField(max_length=100, verbose_name="Отчество", blank=True, null=True)
    email = models.EmailField(verbose_name="Электронная почта")
    comment = models.TextField(verbose_name="Комментарий")

    def __str__(self):
        return f"{self.first_name} {self.last_name}. ({self.comment})"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
