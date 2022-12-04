from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from auth_app.forms import UserRegisterForm


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
            return HttpResponseRedirect(reverse('admin:index'))
