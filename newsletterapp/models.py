from django.db import models

from users.models import Users


class Newsletter(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="user", default=1)

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

    last_send_date = models.DateField(blank=True, null=True, verbose_name="Дата последней отправки")
    send_time = models.TimeField(blank=True, null=True, verbose_name="Время отправки")
    periodicity = models.PositiveIntegerField(verbose_name="Периодичность отправки в днях", default=0)
    next_send_day = models.DateField(verbose_name="Дата ближайшей отправки", blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name="Статус")

    def __str__(self):
        return f"{self.next_send_day}, {self.periodicity}, {self.status}"

    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"


class NewsletterLogs(models.Model):
    newsletter = models.ForeignKey(Newsletter, models.CASCADE, related_name="logs")
    send_date = models.DateField(auto_now_add=True, verbose_name="Дата отправки", blank=True, null=True)
    send_time = models.TimeField(auto_now_add=True, verbose_name="Время отправки", blank=True, null=True)
    send_method = models.CharField(max_length=15, verbose_name="Способ отправки", default="По расписанию")
    status = models.BooleanField(verbose_name="Статус")
    server_answer = models.TextField(verbose_name="Ответ почтового сервера", blank=True, null=True)

    def __str__(self):
        return f"{self.send_date}, {self.status}"

    class Meta:
        verbose_name = "Отправка"
        verbose_name_plural = "История отправок"
