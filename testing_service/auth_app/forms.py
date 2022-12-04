from django.contrib.auth.forms import UserCreationForm

from auth_app.models import User


class UserRegisterForm(UserCreationForm):
    """Форма регистрации"""

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'password1',
                  'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
