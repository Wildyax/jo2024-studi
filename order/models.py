from django.db import models
from django.utils import timezone
from user.models import CustomUser
from offer.models import Offer

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT)
    orderkey = models.CharField(max_length=100)
    stripe_session_id = models.CharField(max_length=255, default='')
    date = models.DateTimeField(default=timezone.now)