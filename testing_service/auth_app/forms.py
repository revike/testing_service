from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from auth_app.models import User


class UserRegisterForm(UserCreationForm):
    """Registration form"""

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'password1',
                  'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''


class UserLoginForm(AuthenticationForm):
    """Authorization form"""

    class Meta:
        model = User
        fields = ('username', 'password')
