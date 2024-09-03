from django.contrib import admin

from newsletterapp.models import Newsletter, NewsletterSettings


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'content')


@admin.register(NewsletterSettings)
class NewsletterSettingsAdmin(admin.ModelAdmin):
    list_display = ('newsletter', 'start_datetime', 'periodicity', 'status')
