from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('lk_test/', views.lk, name='lk_test'),
]

