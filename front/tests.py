from django.test import TestCase
from django.urls import reverse
from .forms import SubscribeForm, LoginForm
from user.models import CustomUser

"""
Test of the Subscribe Form
"""
class SubscribeFormTest(TestCase):

    def test_valid_password(self):
        form = SubscribeForm(data={
            "name": "Doe",
            "first_name": "John",
            "email": "user@example.com",
            "password": "Password1234"
        })
        self.assertTrue(form.is_valid())

    def test_password_too_short(self):
        form = SubscribeForm(data={
            "name": "Doe",
            "first_name": "John",
            "email": "user@example.com",
            "password": "Pass"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)

    def test_password_missing_uppercase(self):
        form = SubscribeForm(data={
            "name": "Doe",
            "first_name": "John",
            "email": "user@example.com",
            "password": "password1"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)

    def test_password_missing_number(self):
        form = SubscribeForm(data={
            "name": "Doe",
            "first_name": "John",
            "email": "user@example.com",
            "password": "Password"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)

    def test_password_with_spaces(self):
        form = SubscribeForm(data={
            "name": "Doe",
            "first_name": "John",
            "email": "user@example.com",
            "password": "Pass word1"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)

"""
Test of the Login Form
"""
class LoginFormTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='user@example.com', password='Password1234')

    def test_login_success(self):
        response = self.client.post(reverse('subscribe'), {
            'email': 'user@example.com',
            'password': 'Password1234',
            'form-name': 'login'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_fail_wrong_password(self):
        response = self.client.post(reverse('subscribe'), {
            'email': 'user@example.com',
            'password': 'WrongPass',
            'form-name': 'login'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Votre mot de passe doit contenir au moins 8")
    
    def test_login_fail_no_user(self):
        response = self.client.post(reverse('subscribe'), {
            'email': 'nouser@example.com',
            'password': 'Password123',
            'form-name': 'login'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Votre mot de passe doit contenir au moins 8")