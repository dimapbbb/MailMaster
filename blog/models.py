from django.db import models

from users.models import Users


class BlogPost(models.Model):
    choices = [
        ('pub', 'Опубликовано'),
        ('no_pub', 'Не опубликовано'),
        ('work', 'На проверке менеджера')
    ]
    user = models.ForeignKey(Users, on_delete=models.SET_DEFAULT, default=1)

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    image = models.FileField(upload_to='blog_image/', verbose_name="Картинка", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", blank=True, null=True)
    published_date = models.DateField(verbose_name="Дата публикации", blank=True, null=True)
    published_sign = models.CharField(choices=choices, default='no_pub', verbose_name="Знак публикации")

    views_count = models.PositiveIntegerField(default=0, verbose_name="Просмотры")

    def __str__(self):
        return f"{self.title} ({self.user})"

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Блог"
