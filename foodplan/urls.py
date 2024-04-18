from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='start_page'),
    path('lk_test/', views.lk, name='lk_test'),
]

