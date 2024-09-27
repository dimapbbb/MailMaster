from django import forms

from blog.models import BlogPost
from newsletterapp.forms import StyleFormMixin


class PostForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ('title', 'content', 'image')
