from django import forms

from blog.models import BlogPost


class PostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ('title', 'content', 'image')
