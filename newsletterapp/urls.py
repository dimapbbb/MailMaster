from django.urls import path

from newsletterapp.apps import NewsletterappConfig
from newsletterapp.views import (home,
                                 NewsletterListView,
                                 NewsletterCreateView,
                                 NewsletterUpdateView,
                                 NewsletterDetailView,
                                 NewsletterDeleteView)

app_name = NewsletterappConfig.name


urlpatterns = [
    path('', home, name='home'),
    path('newsletters/', NewsletterListView.as_view(), name="list"),
    path('create/', NewsletterCreateView.as_view(), name="create"),
    path('update/<int:pk>/', NewsletterUpdateView.as_view(), name="update"),
    path('read/<int:pk>/', NewsletterDetailView.as_view(), name="read"),
    path('delete/<int:pk>/', NewsletterDeleteView.as_view(), name="delete"),
]
