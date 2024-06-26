from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='start_page'),
    path('lk/', views.lk, name='lk'),
    path('recipe/', views.recipe, name='recipe'),
    path('reaction_recipe/', views.reaction_recipe, name='reaction_recipe'),
    path('change_recipe/', views.change_recipe, name='change_recipe'),
    path('subscription/', views.subscription, name='subscription'),
    path('create_subscription/', views.create_subscription,
         name='create_subscription'),
    path('answer_yookassa', views.answer_yookassa, name='answer_yookassa')
]

