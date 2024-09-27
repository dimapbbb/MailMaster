from django.contrib import admin
from recepients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'comment')
