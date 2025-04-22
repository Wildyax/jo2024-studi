from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('logout', views.log_out, name='log_out'),
    path('offers', views.offers, name='offers'),
    path('payment', views.payment, name='payment'),
    path('order-confirm/<str:order_id>/', views.order_confirm, name='order_confirm'),
    path('generate-ticket/<str:order_id>/', views.generate_ticket, name='generate_ticket'),
    path('account', views.account, name='account'),

    # Cart routes
    path('add-to-cart', views.add_to_cart, name='add_to_cart'),
    path('clear-cart', views.clear_cart, name='clear_cart'),
    path('cart', views.show_cart, name='show_cart'),
]