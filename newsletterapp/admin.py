from django.contrib import admin

from newsletterapp.models import Newsletter, NewsletterSettings


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'topic', 'content')


@admin.register(NewsletterSettings)
class NewsletterSettingsAdmin(admin.ModelAdmin):
    list_display = ('newsletter', 'start_date', 'send_time', 'periodicity', 'next_send_day', 'status')
