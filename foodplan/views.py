import datetime
import json
import random


from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.forms.models import model_to_dict

from .models import Subscription, MenuType, MealType, Allergy

from foodplan.models import Subscription, SubscriptionMealType, Recipe, UserRecipe
from .serializers import UserRecipeSerializer


def index(request):
    return render(request,
                  'foodplan/index.html',
                  )


@login_required
def lk(request):
    active_subscriptions = request.user.subscriptions.filter(
        end_date__gte=datetime.date.today()
    )

    total_user_recipes = []
    if active_subscriptions:
        date = datetime.date.today()
        user_dislike_recipes = UserRecipe.objects.filter(user=request.user, reaction='dislike').values_list(
            'recipe__pk', flat=True)
        for subscription in active_subscriptions:
            user_recipes = UserRecipe.objects.filter(date=date, subscription_id=subscription.id, is_valid=True)
            if not user_recipes:
                for subscription_meal_type in subscription.subscription_meal_types.all():
                    meal_type = subscription_meal_type.meal_type
                    menu_type = subscription.menu_type
                    allergies = subscription.allergies.all()
                    possible_recipes = Recipe.objects.filter(
                        menu_type=menu_type,
                        meal_type=meal_type,
                    ).exclude(
                        ingredients__allergy__in=allergies,
                    ).exclude(
                        pk__in=user_dislike_recipes,
                    ).exclude(
                        pk__in=user_dislike_recipes,
                    )
                    random_recipe = random.choice(possible_recipes)

                    new_recipe = UserRecipe.objects.create(
                        user=request.user,
                        date=date,
                        meal_type=meal_type,
                        recipe=random_recipe,
                        subscription=subscription,
                        multiplier=(subscription.people_quantity + (random_recipe.people - 1)) // random_recipe.people,
                    )
                    total_user_recipes.append(new_recipe)
            else:
                total_user_recipes += user_recipes

    return render(request, 'foodplan/lk.html',
                  context={
                      'active_subscriptions': active_subscriptions,
                      'username': request.user.username,
                      'user_recipes': total_user_recipes,
                  }
                  )

@login_required
def subscription(request):
    return render(request, 'foodplan/order.html',)


@api_view(['GET',])
@login_required
def create_subscription(request):
    menu_type = int(request.GET.get('menu_type', '1'))  # ID menu_type
    period = int(request.GET.get('period', '0'))        # в месяцах
    meal_types = [1-int(request.GET.get('select1', '0')),
                  1-int(request.GET.get('select2', '0')),
                  1-int(request.GET.get('select3', '0')),
                  1-int(request.GET.get('select4', '0'))]
    meals = 0
    for meal in meal_types:
        meals += meal
    persons = int(request.GET.get('persons', '1'))      # кол-во человек

    allergy_types = [int(request.GET.get('allergy1', '0')),
                     int(request.GET.get('allergy2', '0')),
                     int(request.GET.get('allergy3', '0')),
                     int(request.GET.get('allergy4', '0')),
                     int(request.GET.get('allergy5', '0')),
                     int(request.GET.get('allergy6', '0'))]

    if ((period < 1) or (menu_type not in range(1, 5)) or (not meals)
        or (persons < 1)):
        return redirect('subscription')
    
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=period*30)
    subscription, created = Subscription.objects.get_or_create(
        user=request.user,
        menu_type=MenuType.objects.get(pk=menu_type),
        people_quantity=persons,
        total_price=(meals*10+65)*persons,
        start_date=start_date,
        end_date=end_date,
    )
    if (created):
        for meal_pk, value in enumerate(meal_types):
            if value:
                meal = MealType.objects.get(pk=meal_pk+1)
                subscription.meal_type.add(meal)
        for allergy_pk, value in enumerate(allergy_types):
            if value:
                allergy = Allergy.objects.get(pk=allergy_pk+1)
                subscription.allergies.add(allergy)

    return Response({'status': f"{period < 1} {menu_type not in range(1, 5)} {meals} {persons < 1}"})

@require_POST
@login_required
def reaction_recipe(request):
    data = json.loads(request.body)
    recipe_id = data.get('recipe_id')
    reaction = data.get('reaction')
    user_recipe = UserRecipe.objects.get(pk=recipe_id)
    user_recipe.reaction = reaction
    user_recipe.save()
    return JsonResponse({'status': 'success'})


@require_POST
@login_required
def change_recipe(request):
    data = json.loads(request.body)
    recipe_id = data.get('recipe_id')
    user_recipe = UserRecipe.objects.get(pk=recipe_id)
    user_dislike_recipes = UserRecipe.objects.filter(user=request.user, reaction='dislike').values_list(
        'recipe__pk', flat=True)
    subscription = user_recipe.subscription
    meal_type = user_recipe.meal_type
    menu_type = subscription.menu_type
    allergies = subscription.allergies.all()
    possible_recipes = Recipe.objects.filter(
        menu_type=menu_type,
        meal_type=meal_type,
    ).exclude(
        ingredients__allergy__in=allergies,
    ).exclude(
        pk__in=user_dislike_recipes,
    ).exclude(
        pk__in=user_dislike_recipes,
    )
    random_recipe = random.choice(possible_recipes)

    user_recipe.is_valid = False
    user_recipe.save()

    new_recipe = UserRecipe.objects.create(
        user=request.user,
        date=user_recipe.date,
        meal_type=meal_type,
        recipe=random_recipe,
        subscription=subscription,
        attempt=user_recipe.attempt + 1,
        multiplier=(subscription.people_quantity + (random_recipe.people - 1)) // random_recipe.people,
    )
    serializer = UserRecipeSerializer(new_recipe)

    return JsonResponse({'status': 'success',
                         'new_recipe': serializer.data,})
