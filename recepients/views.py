from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from recepients.models import Client


class ClientListView(ListView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Список получателей"
        return context


class ClientCreateView(CreateView):
    model = Client
    fields = ('last_name', 'first_name', 'sur_name', 'email', 'comment')
    success_url = reverse_lazy('recipients:clients')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новый получатель"
        return context


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('last_name', 'first_name', 'sur_name', 'email', 'comment')

    def get_success_url(self):
        return reverse('recipients:client_detail', args=[self.kwargs.get('pk')])


class ClientDetailView(DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = kwargs.get('object').last_name
        return context


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('recipients:clients')
