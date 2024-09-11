import random

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView

from config import settings
from users.forms import UserRegisterForm
from users.models import Users


class RegisterView(CreateView):
    model = Users
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get_success_url(self):
        return reverse_lazy('users:login')


class LogoutUserView(TemplateView):
    template_name = 'users/logout.html'

    def post(self, request):
        request.session.delete()
        return redirect('newsletter:home')
