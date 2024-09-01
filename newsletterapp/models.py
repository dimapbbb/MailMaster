from django.db import models


class Newsletter(models.Model):

    title = models.CharField(max_length=50, verbose_name="Заголовок")
    topic = models.CharField(max_length=200, verbose_name="Тема рассылки")
    content = models.TextField(verbose_name="Содержимое рассылки")

    def __str__(self):
        return f"{self.title}, {self.topic}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

