from django.contrib import admin

from newsletterapp.models import Newsletter, NewsletterSettings, NewsletterLogs


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'topic', 'content')


@admin.register(NewsletterSettings)
class NewsletterSettingsAdmin(admin.ModelAdmin):
    list_display = ('newsletter', 'last_send_date', 'send_time', 'periodicity', 'next_send_day', 'status')


@admin.register(NewsletterLogs)
class NewsletterLogsAdmin(admin.ModelAdmin):
    list_display = ('newsletter', 'send_date', 'send_time', 'status', 'server_answer')
