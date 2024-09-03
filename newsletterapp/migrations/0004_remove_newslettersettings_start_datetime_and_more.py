# Generated by Django 5.0.7 on 2024-09-03 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletterapp', '0003_newslettersettings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newslettersettings',
            name='start_datetime',
        ),
        migrations.AddField(
            model_name='newslettersettings',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата и время начала'),
        ),
    ]
