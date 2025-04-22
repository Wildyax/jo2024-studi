from django.test import TestCase, Client
from offer.models import Offer
from user.models import CustomUser
from .utils import get_test_image

"""
Tests of offers edition in back-office 
"""
class OfferBackOfficeTests(TestCase):
    
    def setUp(self):
        self.admin = CustomUser.objects.create_user(
            email="admin@example.com",
            password="adminpassword",
            is_staff=True
        )
        self.client = Client()
        self.client.login(email="admin@example.com", password="adminpassword")

    def test_create_offer(self):
        response = self.client.post(
            '/back-office/offers/save',
            {
                'offer-id': 0,
                'title': 'Offre Test',
                'description': 'Ceci est une offre test',
                'price': '49.99',
                'places': 2,
                'image': get_test_image(),
            }
        )
       
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Offer.objects.filter(title='Offre Test').exists())

    def test_edit_offer(self):
        offer = Offer.objects.create(
            title='Offre Originale',
            description='Ancienne description',
            price=30.00,
            places=1,
            image=get_test_image(),
        )

        response = self.client.post(
            '/back-office/offers/save',
            {
                'offer-id': offer.id,
                'title': 'Offre Modifiée',
                'description': 'Nouvelle description',
                'price': '60.00',
                'places': 3,
                'image': get_test_image(),
            }
        )

        self.assertEqual(response.status_code, 200)
        offer.refresh_from_db()
        self.assertEqual(offer.title, 'Offre Modifiée')
        self.assertEqual(offer.price, 60.00)

    def test_delete_offer(self):
        offer = Offer.objects.create(
            title='Offre à supprimer',
            description='Bientôt supprimée',
            price=20.00,
            places=2,
            image=get_test_image(),
        )

        response = self.client.get(f'/back-office/offers/delete?offer-id={offer.id}')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Offer.objects.filter(id=offer.id).exists())