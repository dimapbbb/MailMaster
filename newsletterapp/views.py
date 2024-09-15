from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, TemplateView

from newsletterapp.forms import NewsletterForm, NewsletterSettingsForm
from newsletterapp.models import Newsletter, NewsletterSettings, NewsletterLogs
from newsletterapp.utils import send_newsletter


def home(request):
    context = {
        "title": "Мастер рассылок",
        "description": "это отличный вариант для доставки важной информации по электронной почте"
    }
    return render(request, 'newsletterapp/home.html', context)


class NewsletterListView(ListView):
    model = Newsletter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Мои рассылки"
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        state = self.kwargs.get('state')
        if state == 'activ':
            queryset = queryset.filter(newslettersettings__status=True)
        elif state == 'not_activ':
            queryset = queryset.filter(newslettersettings__status=False)

        for obj in queryset:
            newsletter = NewsletterSettings.objects.get(newsletter=obj.pk)
            obj.status = newsletter.status
            obj.last_send_date = newsletter.last_send_date
            obj.next_send_day = newsletter.next_send_day
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
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('newsletter:newsletters_list', args=['all'])


class NewsletterUpdateView(UpdateView):
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


class NewsletterDetailView(DetailView):
    model = Newsletter

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        newsletter_id = self.kwargs.get('pk')
        settings = NewsletterSettings.objects.get(newsletter=newsletter_id)

        self.object.last_send_date = settings.last_send_date

        self.object.send_time = settings.send_time

        self.object.next_send_day = settings.next_send_day

        if settings.periodicity:
            self.object.periodicity = f"Раз в {settings.periodicity} дней"

        else:
            self.object.periodicity = "Отключена"

        if settings.status:
            self.object.status = "Активная"
        else:
            self.object.status = "Не активная"
            self.object.next_send_day = "Отключена"

        self.object.save()
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = kwargs.get('object').title
        return context


class NewsletterDeleteView(DeleteView):
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


class ConfirmSend(TemplateView):
    template_name = "newsletterapp/confirm_send.html"

    def post(self, request, **kwargs):
        """ Обработка POST запроса"""
        context = super().get_context_data(**kwargs)
        pk = context.get('pk')
        send_newsletter(pk, send_method="Ручная отправка")
        return redirect('newsletter:newsletters_list', context)
