from django import forms
from newsletterapp.forms import StyleFormMixin
from recepients.models import Client


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = ('last_name', 'first_name', 'sur_name', 'email', 'comment')
