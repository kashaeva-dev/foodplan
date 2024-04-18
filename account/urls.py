from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.urls import path

from account.views import RegistrationUser, LoginUser

app_name = "account"
urlpatterns = [
    path('registration/', RegistrationUser.as_view(), name='registration'),
    path('auth/', LoginUser.as_view(), name='auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', render, kwargs={"template_name": "foodplan/lk.html"}, name='profile')
]
