from django.urls import path
from django.views.decorators.cache import cache_page

from recepients.apps import RecepientsConfig
from recepients.views import (ClientListView,
                              ClientCreateView,
                              ClientUpdateView,
                              ClientDetailView,
                              ClientDeleteView)

app_name = RecepientsConfig.name


urlpatterns = [
    path('clients/', cache_page(60)(ClientListView.as_view()), name='clients'),
    path('add_client/', ClientCreateView.as_view(), name='add_client'),
    path('update_client/<int:pk>', ClientUpdateView.as_view(), name='update_client'),
    path('client_detail/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
]
