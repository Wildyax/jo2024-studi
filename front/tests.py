from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import SubscribeForm, LoginForm
from user.models import CustomUser
from offer.models import Offer
from order.models import Order  
from unittest.mock import patch
from .utils import get_test_image

"""
Test of the purchase flow from login to purchase
"""
class PurchaseTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="Password1234"
        )
        self.offer = Offer.objects.create(
            title="Duo",
            description="Partagez l'émotion des Jeux à deux ! Un moment unique à vivre avec la personne de votre choix.",
            price=200.00,
            places=2,
            image=get_test_image()
        )
    
    def test_purchase_flow(self):
        # User login test
        self.client.login(email="user@example.com", password="Password1234")

        # Add offer to cart with AJAX
        response = self.client.get(reverse('add_to_cart'), {'offer_id': self.offer.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn('offer', self.client.session['cart'])

        # Access payment page
        response = self.client.get(reverse('payment'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.offer.title)

        # Change Stripe session object to a fake one for tests
        with patch("front.views.stripe.checkout.Session.create") as mock_create_session:
            mock_create_session.return_value.url = "/fake-stripe-url"
            response = self.client.get(reverse('create_checkout_session'))
            self.assertEqual(response.status_code, 302)
            self.assertIn("/fake-stripe-url", response.url)

        # Simulate a success payment from Stripe
        session_id = "fake-session-id"
        with patch("front.views.stripe.checkout.Session.retrieve") as mock_retrieve_session:
            mock_retrieve_session.return_value.payment_status = "paid"
            response = self.client.get(
                reverse('success_checkout_session') + f"?session_id={session_id}"
            )

        # Check redirection and order
        self.assertEqual(response.status_code, 302)
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.offer, self.offer)
        self.assertEqual(order.stripe_session_id, session_id)

        # Check the cart clear
        self.assertEqual(self.client.session.get('cart'), {})



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