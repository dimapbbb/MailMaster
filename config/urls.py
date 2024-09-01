from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('newsletterapp.urls', namespace='newsletter')),
    path('recipients/', include('recepients.urls', namespace='recipients')),
]
