from django.shortcuts import render
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from newsletterapp.forms import NewsletterForm, NewsletterSettingsForm
from newsletterapp.models import Newsletter, NewsletterSettings


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


class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter:newsletters_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новая рассылка"

        NewsletterSettingsFormset = inlineformset_factory(Newsletter, NewsletterSettings, form=NewsletterSettingsForm)
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

            # При создании автоматически сохраняет дату след отправки равной дате первой отправки
            settings = NewsletterSettings.objects.get(newsletter=self.object.pk)
            settings.next_send_day = settings.start_date
            settings.save()

        return super().form_valid(form)


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    form_class = NewsletterSettingsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование"

        NewsletterSettingsFormset = inlineformset_factory(Newsletter, NewsletterSettings, form=NewsletterSettingsForm)
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
        self.object.start_date = settings.start_date
        self.object.send_time = settings.send_time
        self.object.periodicity = settings.periodicity
        self.object.next_send_day = settings.next_send_day
        if settings.status:
            self.object.status = "Активная"
        else:
            self.object.status = "Не активная"
        self.object.save()
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = kwargs.get('object').title
        return context


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    success_url = reverse_lazy('newsletter:newsletters_list')
