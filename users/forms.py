from django.contrib.auth.forms import UserCreationForm

from users.models import Users


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = Users
        fields = ('username', 'email')
