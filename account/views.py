from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from account.forms import RegistrationUserForm, AuthorizationUserForm


class RegistrationUser(CreateView):
    form_class = RegistrationUserForm
    template_name = 'foodplan/registration.html'
    success_url = reverse_lazy("account:auth")


class LoginUser(LoginView):
    form_class = AuthorizationUserForm
    template_name = 'foodplan/auth.html'

