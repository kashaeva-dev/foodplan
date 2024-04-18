from django.urls import reverse_lazy
from django.views.generic import CreateView

from account.forms import RegistrationUserForm


class RegistrationUser(CreateView):
    form_class = RegistrationUserForm
    template_name = 'foodplan/registration.html'
    success_url = reverse_lazy("account:auth")
# def register_user(request):
#     form = None
#     if request.method == 'POST':
#         form = RegistrationUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data["password"])
#             user.save()
#             return render(request, 'foodplan/registration_done.html')
#     elif request.method == 'GET':
#         form = RegistrationUserForm()
#     return render(request, 'foodplan/registration.html', {'form': form})
