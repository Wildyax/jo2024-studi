from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('logout', views.logOut, name='logout')
]