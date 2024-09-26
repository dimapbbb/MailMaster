from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView
from django.contrib.auth.mixins import AccessMixin

from blog.models import BlogPost
from config import settings
from newsletterapp.models import Newsletter, NewsletterSettings
from recepients.models import Client
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import Users


class UserAccessMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        owner_data = Users.objects.get(id=kwargs.get('pk'))
        if request.user == AnonymousUser():
            return render(request, 'newsletterapp/home.html')
        elif request.user != owner_data:
            return render(request, 'error_message.html')
        else:
            return super().dispatch(request, *args, **kwargs)


class ManagerRequiredMixin(AccessMixin):
    """Verify that the current user is Manager."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_manager():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    model = Users
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get_success_url(self):
        return reverse_lazy('newsletterapp:home')

    def form_valid(self, form):
        if form.is_valid:
            user = form.save()
            user.is_active = False
            user.save()

            link = f'http://127.0.0.1:8000/confirm_email/{user.pk}'

            send_mail(
                "Регистрация нового пользователя",
                f"Для продолжения перейдите по ссылке: {link}",
                settings.EMAIL_HOST_USER,
                [user.email]
            )

        return super().form_valid(form)


class ConfirmEmailView(UserAccessMixin, TemplateView):
    template_name = 'users/confirm_email.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")

        user = Users.objects.get(id=pk)
        user.is_active = True
        user.save()

        return super().get(request, *args, **kwargs)


class LogoutUserView(TemplateView):
    template_name = 'users/logout.html'

    @staticmethod
    def post(request):
        request.session.delete()
        return redirect('newsletter:home')


class UsersDetailView(UserAccessMixin, DetailView):
    model = Users

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        obj = Users.objects.get(pk=pk)

        newsletters = Newsletter.objects.filter(user_id=pk)
        active_newsletters_count = newsletters.filter(newslettersettings__status=True).count()
        newsletters_count = newsletters.count()
        clients_count = Client.objects.filter(user_id=pk).count()

        public_posts = BlogPost.objects.filter(user_id=pk, published_sign=True)
        all_views_count = sum([post.views_count for post in public_posts])

        obj.newsletters_count = newsletters_count
        obj.active_newsletters_count = active_newsletters_count
        obj.clients_count = clients_count
        obj.public_posts_count = public_posts.count()
        obj.views_count = all_views_count

        return obj


class UsersUpdateView(UserAccessMixin, UpdateView):
    model = Users
    form_class = UserUpdateForm
    template_name = "users/users_update.html"

    def get_success_url(self):
        return reverse('users:users_detail', args=[self.kwargs.get("pk")])


class UsersDeleteView(UserAccessMixin, TemplateView):
    model = Users
    template_name = "users/users_confirm_delete.html"

    @staticmethod
    def post(request, pk):
        user = request.user
        user.is_active = False
        user.save()
        return redirect('newsletter:home')


class UsersBlockView(ManagerRequiredMixin, TemplateView):
    template_name = 'users/confirm_block.html'

    def post(self, *args, **kwargs):
        pk = kwargs.get('pk')
        newsletter = Newsletter.objects.get(id=pk)
        user = newsletter.user

        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()

        return redirect('newsletter:newsletter_read', pk=pk)
