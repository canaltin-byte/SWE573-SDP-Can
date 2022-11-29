from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
# Create your tests here.

class Testing(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_login_will_pass(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345can')
        user.save()

        c = Client()
        logged_in = c.login(username='testuser', password='12345can')
        self.assertTrue(logged_in)

    def test_login_will_fail(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345can')
        user.save()

        c = Client()
        logged_in = c.login(username='testuser', password='12345')
        self.assertTrue(logged_in)
