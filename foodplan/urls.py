from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='start_page'),
    path('lk_test/', views.lk, name='lk_test'),
    path('reaction_recipe/', views.reaction_recipe, name='reaction_recipe'),
    path('subscription/', views.subscription, name='subscription'),
    path('create_subscription/', views.create_subscription,
         name='create_subscription'),
]

