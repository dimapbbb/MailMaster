from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from newsletterapp.forms import StyleFormMixin

from users.models import Users


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = Users
        fields = ('username', 'email')


class UserUpdateForm(StyleFormMixin, UserChangeForm):

    class Meta:
        model = Users
        fields = ('photo', 'first_name', 'last_name', 'username')
