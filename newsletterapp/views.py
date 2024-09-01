from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from newsletterapp.models import Newsletter


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
    fields = ('title', 'topic', 'content')
    success_url = reverse_lazy('newsletter:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новая рассылка"
        return context


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    fields = ('title', 'topic', 'content')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Изменить"
        return context

    def get_success_url(self):
        return reverse('newsletter:read', args=[self.kwargs.get('pk')])


class NewsletterDetailView(DetailView):
    model = Newsletter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = kwargs.get('object').title
        return context


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    success_url = reverse_lazy('newsletter:list')
