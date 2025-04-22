from django.urls import path

from . import views

urlpatterns = [
    path('', views.back_office, name='back_office'),

    path('offers', views.offers, name='offers'),
    path('offers/edit', views.edit_offer, name='edit_offer'),
    path('offers/save', views.save_offer, name='save_offer'),
    path('offers/delete', views.delete_offer, name='delete_offer'),

    path('orders', views.orders, name='orders'),
]