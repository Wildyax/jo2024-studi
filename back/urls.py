from django.urls import path

from . import views

urlpatterns = [
    path('', views.backOffice, name='back-office'),
    path('offers', views.offers, name='offers'),
    path('offers/edit', views.editOffer, name='offerEdit'),
    path('offers/save', views.saveOffer, name='offerSave'),
    path('offers/delete', views.deleteOffer, name='offerDelete'),
]