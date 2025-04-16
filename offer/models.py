from django.db import models

# Create your models here.
class Offer(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    places = models.PositiveIntegerField()
    image = models.ImageField(upload_to='offers/')