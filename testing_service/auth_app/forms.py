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
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            field.label = ''
        self.fields['username'].widget.attrs[
            'placeholder'] = 'Имя пользователя'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password2'].widget.attrs[
            'placeholder'] = 'Повторите пароль'


class UserLoginForm(AuthenticationForm):
    """Authorization form"""

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            field.label = ''
        self.fields['username'].widget.attrs[
            'placeholder'] = 'Имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль'
