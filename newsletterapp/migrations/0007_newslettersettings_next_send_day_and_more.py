# Generated by Django 5.0.7 on 2024-09-04 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletterapp', '0006_newslettersettings_send_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='newslettersettings',
            name='next_send_day',
            field=models.DateField(blank=True, null=True, verbose_name='Дата следующей отправки'),
        ),
        migrations.AlterField(
            model_name='newslettersettings',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата первой отправки'),
        ),
    ]
