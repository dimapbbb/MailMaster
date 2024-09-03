from django.db import models


class Client(models.Model):
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