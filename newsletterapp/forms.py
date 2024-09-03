from django import forms

from newsletterapp.models import Newsletter, NewsletterSettings


class NewsletterForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ('title', 'topic', 'content')


class NewsletterSettingsForm(forms.ModelForm):

    class Meta:
        model = NewsletterSettings
        fields = ('start_date', 'send_time', 'periodicity', 'status')
