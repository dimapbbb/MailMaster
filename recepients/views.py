from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from recepients.models import Client


class UserAccessMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        owner_data = Client.objects.get(id=kwargs.get('pk')).user
        if request.user == AnonymousUser():
            return render(request, 'newsletterapp/home.html')
        elif request.user.is_manager():
            return super().dispatch(request, *args, **kwargs)
        elif request.user != owner_data:
            return render(request, 'error_message.html')
        else:
            return super().dispatch(request, *args, **kwargs)


class ClientListView(ListView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Список получателей"
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).filter(user=self.request.user.pk)

        return queryset


class ClientCreateView(CreateView):
    model = Client
    fields = ('last_name', 'first_name', 'sur_name', 'email', 'comment')
    success_url = reverse_lazy('recipients:clients')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новый получатель"
        return context

    def form_valid(self, form):
        obj = form.save()
        obj.user = self.request.user
        obj.save()

        return super().form_valid(form)


class ClientUpdateView(UserAccessMixin, UpdateView):
    model = Client
    fields = ('last_name', 'first_name', 'sur_name', 'email', 'comment')

    def get_success_url(self):
        return reverse('recipients:client_detail', args=[self.kwargs.get('pk')])


class ClientDetailView(UserAccessMixin, DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = kwargs.get('object').last_name
        return context


class ClientDeleteView(UserAccessMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('recipients:clients')
