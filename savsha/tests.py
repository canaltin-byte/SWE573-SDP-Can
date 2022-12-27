from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.contrib.auth import authenticate

# Create your tests here.
from django.urls import reverse


class Testing(TestCase):
    def setUp(self):
        # Setup run before every test method
        self.register_url = reverse('register')
        self.new_content_url = reverse('new_content')
        self.user = {
            'username': 'testcase',
            'email': 'testcase@gmail.com',
            'password1': 'sifre123',
            'password2': 'sifre123',
        }
        self.user2 = {
            'username': 'testcase2',
            'email': 'testcase@gmail.com',
            'password1': 'testcase2',
            'password2': 'testcase2',
        }
        self.user3 = {
            'username': 'testcase3',
            'email': 'testcase@gmail.com',
            'password1': 'denemecase2',
            'password2': '',
        }
        self.content = {
            'user_id': 100,
            'first_name': 'Imaginary',
            'last_name': 'Person',
            'title': 'Person',
            'message': 'Person',
            'address': 'Person',
            'labels': 'Person',
            'origin': 'Person',
            'privacy': False,
        }
        dummy_user = User()
        dummy_user.username = 'testuser'
        dummy_user.set_password('dummypass')
        dummy_user.email = 'testemail@gmail.com'
        dummy_user.save()
        return super().setUp()

    def tearDown(self):
        # Clean up run after every test method.
        dummy_user = User.objects.all().filter(username='testuser')
        dummy_user.delete()
        dummy_user = User.objects.all().filter(username='testcase')
        dummy_user.delete()
        dummy_user = User.objects.all().filter(username='testcase2')
        dummy_user.delete()
        dummy_user = User.objects.all().filter(username='testcase3')
        dummy_user.delete()

    def test_login_will_pass(self):
        logged_in = authenticate(username='testuser', password='dummypass')
        self.assertTrue(logged_in)

    def test_login_will_fail(self):
        logged_in = authenticate(username='testuser', password='12345')
        self.assertFalse(logged_in)

    def test_register_will_pass(self):
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_register_same_password_username_will_fail(self):
        response = self.client.post(self.register_url, self.user2, format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_register_missing_data_will_fail(self):
        response = self.client.post(self.register_url, self.user3, format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_new_content_will_pass(self):
        response = self.client.post(self.new_content_url, self.content, format='text/html')
        self.assertEqual(response.status_code, 200)
