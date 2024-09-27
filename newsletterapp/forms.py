from datetime import datetime, timedelta

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
        self.fields.get('next_send_day').widget.attrs.update({"min": datetime.now().date(),
                                                              "required": True})
        self.fields.get('send_time').widget.attrs.update({"required": True})

    def clean(self):
        day = self.cleaned_data.get('next_send_day')
        time = self.cleaned_data.get('send_time')
        if day == datetime.now().date() and time < datetime.now().time():
            self.cleaned_data['next_send_day'] += timedelta(days=1)
        return self.cleaned_data
