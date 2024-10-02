from random import sample

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, TemplateView
from django.contrib.auth.mixins import AccessMixin

from blog.models import BlogPost
from newsletterapp.forms import NewsletterForm, NewsletterSettingsForm
from newsletterapp.models import Newsletter, NewsletterSettings, NewsletterLogs
from newsletterapp.services import get_cache_data
from newsletterapp.utils import send_newsletter
from recepients.models import Client


class HomeView(TemplateView):
    template_name = 'newsletterapp/home.html'

    def get_context_data(self, **kwargs):
        clients = get_cache_data(key='clients', model=Client)
        newsletters = get_cache_data(key='newsletters', model=Newsletter)
        all_posts = get_cache_data(key='all_posts', model=BlogPost)

        all_posts = all_posts.filter(published_sign='pub')

        if all_posts is None:
            all_posts = []

        if len(all_posts) < 3:
            random_posts = sample(list(all_posts), k=len(all_posts))
        else:
            random_posts = sample(list(all_posts), k=3)

        context = super().get_context_data(**kwargs)
        context['title'] = "Мастер рассылок"
        context['description'] = (f"Создано {newsletters.count()} рассылок, из них "
                                  f"{newsletters.filter(newslettersettings__status=True).count()} активно рассылают "
                                  f"информацию {clients.count()} клиентам")
        context['random_posts'] = random_posts

        return context


class UserAccessMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        owner_data = Newsletter.objects.get(id=kwargs.get('pk')).user
        if request.user == AnonymousUser():
            return render(request, 'newsletterapp/home.html')
        elif request.user.is_manager():
            return super().dispatch(request, *args, **kwargs)
        elif request.user != owner_data:
            return render(request, 'error_message.html')
        else:
            return super().dispatch(request, *args, **kwargs)


class NewsletterListView(ListView):
    model = Newsletter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Мои рассылки"
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        if not self.request.user.is_manager():
            queryset = queryset.filter(user=self.request.user.pk)

        state = self.kwargs.get('state')
        if state == 'activ':
            queryset = queryset.filter(newslettersettings__status=True)
        elif state == 'not_activ':
            queryset = queryset.filter(newslettersettings__status=False)

        for obj in queryset:
            settings = NewsletterSettings.objects.get(newsletter=obj.pk)
            obj.status = settings.status
            obj.last_send_date = settings.last_send_date
            obj.next_send_day = settings.next_send_day
            obj.content = obj.content[:100] + " . . ."
        return queryset


class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = NewsletterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новая рассылка"

        NewsletterSettingsFormset = inlineformset_factory(Newsletter,
                                                          NewsletterSettings,
                                                          form=NewsletterSettingsForm,
                                                          can_delete=False)

        if self.request.method == "POST":
            context["formset"] = NewsletterSettingsFormset(self.request.POST)
        else:
            context["formset"] = NewsletterSettingsFormset()
        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save(commit=False)
        self.object.user = self.request.user

        if formset.is_valid():
            formset.instance = self.object
            self.object.save()
            formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('newsletter:newsletters_list', args=['all'])


class NewsletterUpdateView(UserAccessMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование"

        NewsletterSettingsFormset = inlineformset_factory(Newsletter,
                                                          NewsletterSettings,
                                                          form=NewsletterSettingsForm,
                                                          can_delete=False)

        if self.request.method == "POST":
            context["formset"] = NewsletterSettingsFormset(self.request.POST, instance=self.object)
        else:
            context["formset"] = NewsletterSettingsFormset(instance=self.object)
        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('newsletter:newsletter_read', args=[self.kwargs.get('pk')])


class NewsletterDetailView(UserAccessMixin, DetailView):
    model = Newsletter

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        newsletter_id = self.kwargs.get('pk')
        settings = NewsletterSettings.objects.get(newsletter=newsletter_id)

        obj.last_send_date = settings.last_send_date
        obj.send_time = settings.send_time
        obj.next_send_day = settings.next_send_day

        if settings.periodicity:
            obj.periodicity = f"Раз в {settings.periodicity} дней"
        else:
            obj.periodicity = "Отключена"

        obj.status = settings.status

        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = kwargs.get('object').title
        return context

    def post(self, *args, **kwargs):
        pk = kwargs.get('pk')
        settings = NewsletterSettings.objects.get(newsletter_id=pk)

        if settings.status:
            settings.status = False
        else:
            settings.status = True
        settings.save()

        return redirect('newsletter:newsletter_read', pk=pk)


class NewsletterDeleteView(UserAccessMixin, DeleteView):
    model = Newsletter

    def get_success_url(self):
        return reverse('newsletter:newsletters_list', args=['all'])


class NewsletterLogsListView(ListView):
    model = NewsletterLogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('pk'):
            context["title"] = "История рассылки"
        else:
            context["title"] = "История всех отправлений"
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        pk = self.kwargs.get('pk')

        if pk:
            queryset = queryset.filter(newsletter=pk).order_by('-send_date', '-send_time')
        else:
            queryset = queryset.all().order_by('-send_date', '-send_time')

            for obj in queryset:
                newsletter_title = Newsletter.objects.get(id=obj.newsletter_id).title
                obj.title = newsletter_title

        return queryset


class ConfirmSend(UserAccessMixin, TemplateView):
    template_name = "newsletterapp/confirm_send.html"

    def post(self, request, **kwargs):
        """ Обработка POST запроса"""
        context = super().get_context_data(**kwargs)
        pk = context.get('pk')
        send_newsletter(pk, send_method="Ручная отправка")
        return redirect('newsletter:newsletters_list', context)
