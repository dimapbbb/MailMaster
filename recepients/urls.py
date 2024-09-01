from django.urls import path

from recepients.apps import RecepientsConfig
from recepients.views import base

app_name = RecepientsConfig.name


urlpatterns = [
    path('', base)
]