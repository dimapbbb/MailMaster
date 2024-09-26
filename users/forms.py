from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import Users


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = Users
        fields = ('username', 'email')


class UserUpdateForm(UserChangeForm):

    class Meta:
        model = Users
        fields = ('photo', 'first_name', 'last_name', 'username')
