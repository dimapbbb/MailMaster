# Generated by Django 5.0.7 on 2024-09-25 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_blogpost_options_alter_blogpost_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='likes_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Лайки'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='published_sign',
            field=models.BooleanField(default=False, verbose_name='Знак публикации'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='published_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='views_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Просмотры'),
        ),
    ]