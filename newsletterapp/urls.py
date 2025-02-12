from django.urls import path

from newsletterapp.apps import NewsletterappConfig
from newsletterapp.views import (NewsletterListView,
                                 NewsletterCreateView,
                                 NewsletterUpdateView,
                                 NewsletterDetailView,
                                 NewsletterDeleteView,
                                 NewsletterLogsListView,
                                 ConfirmSend, HomeView)

app_name = NewsletterappConfig.name


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('newsletters/<str:state>/', NewsletterListView.as_view(), name="newsletters_list"),
    path('create/', NewsletterCreateView.as_view(), name="newsletter_create"),
    path('update/<int:pk>/', NewsletterUpdateView.as_view(), name="newsletter_update"),
    path('read/<int:pk>/', NewsletterDetailView.as_view(), name="newsletter_read"),
    path('delete/<int:pk>/', NewsletterDeleteView.as_view(), name="newsletter_delete"),
    path('history/<int:pk>/', NewsletterLogsListView.as_view(), name="history"),
    path('confirm_send/<int:pk>/', ConfirmSend.as_view(), name='confirm_send'),
]
