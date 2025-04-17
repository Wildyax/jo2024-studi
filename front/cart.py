# cart.py
from decimal import Decimal
from django.conf import settings
from offer.models import Offer

class Cart:
    
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart


    """
    Add an offer to the cart
    """
    def add(self, offer_id):
        if 'offer' in self.cart:
            if self.cart['offer'] != offer_id:
                self.cart['offer'] = offer_id
        else:
            self.cart['offer'] = offer_id

        self.save()

    """
    Save the cart
    """
    def save(self):
        self.session.modified = True

    """
    Clear the cart
    """
    def clear(self):
        self.session['cart'] = {}
        self.save()

    """
    Get offer in cart
    """
    def getOffer(self):
        if 'offer' in self.cart:
            return Offer.objects.get(id=self.cart['offer'])
        
        return None