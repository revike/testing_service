from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic

from auth_app.forms import UserRegisterForm, UserLoginForm


class RegisterView(generic.CreateView):
    """Registration user"""
    template_name = 'auth_app/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('auth:register')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'регистрация'
        return context

    def form_valid(self, form):
        if form.is_valid():
            username = form.data['username']
            password = form.data['password1']
            form.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(self.request, user)
            return HttpResponseRedirect(reverse('main:list_test'))

    @method_decorator(user_passes_test(lambda u: u.is_anonymous))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class LoginUserView(LoginView):
    """Login user"""
    template_name = 'auth_app/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('auth:register')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'авторизация'
        return context

    def form_valid(self, form):
        if form.is_valid():
            super().form_valid(form)
            return HttpResponseRedirect(reverse('main:list_test'))

    @method_decorator(user_passes_test(lambda u: u.is_anonymous))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
