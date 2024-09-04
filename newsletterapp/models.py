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

    start_date = models.DateField(blank=True, null=True, verbose_name="Дата первой отправки")
    send_time = models.TimeField(blank=True, null=True, verbose_name="Время отправки")
    periodicity = models.PositiveIntegerField(verbose_name="Периодичность отправки в днях", default=0)
    next_send_day = models.DateField(verbose_name="Дата следующей отправки", blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name="Статус")

    def __str__(self):
        return f"{self.start_date}, {self.periodicity}, {self.status}"

    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"
