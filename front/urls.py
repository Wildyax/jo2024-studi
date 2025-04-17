from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('logout', views.logOut, name='logout'),
    path('offers', views.offers, name='offers'),
    path('payment', views.payment, name='payment'),

    # Cart routes
    path('add-to-cart', views.addToCart, name='add-to-cart'),
    path('clear-cart', views.clearCart, name='clear-cart'),
    path('cart', views.showCart, name='show-cart'),
]