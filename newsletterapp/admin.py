from django.contrib import admin

from newsletterapp.models import Newsletter


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'content')
