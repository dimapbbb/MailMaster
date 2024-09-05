from datetime import datetime

from django import forms

from newsletterapp.models import Newsletter, NewsletterSettings


class NewsletterForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ('title', 'topic', 'content')


class NewsletterSettingsForm(forms.ModelForm):

    class Meta:
        model = NewsletterSettings
        fields = ('next_send_day', 'send_time', 'periodicity', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields.get('next_send_day').widget.input_type = "date"
        self.fields.get('send_time').widget.input_type = "time"
