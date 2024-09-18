from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView


from users.forms import UserRegisterForm, UserUpdateForm
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


class UsersDetailView(DetailView):
    model = Users

    def get_object(self, queryset=None):
        obj = Users.objects.get(pk=self.kwargs.get('pk'))

        return obj


class UsersUpdateView(UpdateView):
    model = Users
    form_class = UserUpdateForm
    template_name = "users/users_update.html"

    def get_success_url(self):
        return reverse('users:users_detail', args=[self.kwargs.get("pk")])
