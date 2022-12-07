from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse, resolve

from auth_app.views import LoginUserView, RegisterView, LogoutUser


class TestAuthApp(TestCase):
    """Test for app auth"""

    def setUp(self) -> None:
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()
        self.user = {'username': 'admin', 'password': 'admin'}
        self.not_register = {'username': 'admin', 'password1': 'admin',
                         'password2': 'admin'}
        self.register = {'username': 'admins', 'password1': 'admin',
                             'password2': 'admin'}

    def test_register(self):
        """Test register"""
        url = reverse('auth:register')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'auth_app/register.html')
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('main:list_test'))
        self.assertEqual(response.status_code, 302)
        self.client.post(url, data=self.not_register)
        self.assertEqual(response.status_code, 302)
        self.client.post(url, data=self.register)
        self.assertEqual(response.status_code, 302)
        self.client.post(reverse('auth:login'), data=self.user)
        response = self.client.get(reverse('main:list_test'))
        self.assertEqual(response.status_code, 200)
        self.assertEquals(resolve(url).func.view_class, RegisterView)

    def test_login(self):
        """Test login"""
        url = reverse('auth:login')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'auth_app/login.html')
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('main:list_test'))
        self.assertEqual(response.status_code, 302)
        self.client.post(url, data=self.user)
        response = self.client.get(reverse('main:list_test'))
        self.assertEqual(response.status_code, 200)
        self.assertEquals(resolve(url).func.view_class, LoginUserView)

    def test_logout(self):
        """Test logout"""
        url = reverse('auth:logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.post(reverse('auth:login'), data=self.user)
        response = self.client.get(reverse('main:list_test'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('main:list_test'))
        self.assertEqual(response.status_code, 302)
        self.assertEquals(resolve(url).func.view_class, LogoutUser)
