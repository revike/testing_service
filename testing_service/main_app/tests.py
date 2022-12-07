from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse, resolve

from main_app.views import TestingListView


class TestAuthApp(TestCase):
    """Test for app auth"""

    def setUp(self) -> None:
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()
        self.user = {'username': 'admin', 'password': 'admin'}

    def login_user(self):
        url = reverse('auth:login')
        self.client.post(url, data=self.user)
        return self.client

    def test_list_test(self):
        """Test list_test"""
        url = reverse('main:list_test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.login_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(resolve(url).func.view_class, TestingListView)
        self.assertTemplateUsed(response, 'main_app/list_test.html')

    def test_detail_test(self):
        """Test detail_test"""
        url = reverse('main:detail_test', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.login_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/detail_test.html')

    def test_result_list(self):
        """Test result list"""
        url = reverse('main:result_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.login_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/result_list.html')

    def test_result(self):
        """Test result"""
        url = reverse('main:result', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.login_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
