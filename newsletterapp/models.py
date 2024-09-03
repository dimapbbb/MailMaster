from django.db import models


class Newsletter(models.Model):

    title = models.CharField(max_length=50, verbose_name="Заголовок")
    topic = models.CharField(max_length=200, verbose_name="Тема рассылки")
    content = models.TextField(verbose_name="Содержимое рассылки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", blank=True, null=True)

    def __str__(self):
        return f"{self.title}, {self.topic}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class NewsletterSettings(models.Model):
    newsletter = models.OneToOneField(Newsletter, models.CASCADE)

    start_datetime = models.DateTimeField(blank=True, null=True, verbose_name="Дата и время начала")
    periodicity = models.CharField(max_length=20, verbose_name="Периодичность отправки", blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name="Статус")

    def __str__(self):
        return f"{self.start_datetime}, {self.periodicity}, {self.status}"

    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"
