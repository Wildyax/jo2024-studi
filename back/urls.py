from django.urls import path

from . import views

urlpatterns = [
    path('', views.backOffice, name='back-office'),
]