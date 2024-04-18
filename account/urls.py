from django.shortcuts import render
from django.urls import path

from account.views import RegistrationUser

app_name = "account"
urlpatterns = [
    path('registration/', RegistrationUser.as_view(), name='registration'),
    path('auth/', render, kwargs={"template_name": "foodplan/auth.html"}, name='auth')
]
