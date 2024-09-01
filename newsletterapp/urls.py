from django.urls import path

from newsletterapp.apps import NewsletterappConfig
from newsletterapp.views import home

app_name = NewsletterappConfig.name


urlpatterns = [
    path('', home, name='home')
]
