from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('newsletterapp.urls', namespace='newsletter')),
    path('', include('recepients.urls', namespace='recipients')),
    path('', include('users.urls', namespace='users')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
