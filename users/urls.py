from django.contrib.auth.views import LoginView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, LogoutUserView, UsersDetailView

app_name = UsersConfig.name

urlpatterns = [
    path('new_user/', RegisterView.as_view(), name='new_user'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('user_detail/<int:pk>/', UsersDetailView.as_view(), name='users_detail'),
]