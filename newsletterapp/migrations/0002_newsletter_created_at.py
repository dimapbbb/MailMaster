# Generated by Django 5.0.7 on 2024-09-03 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletterapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания'),
        ),
    ]