import datetime
import random

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from foodplan.models import Subscription, SubscriptionMealType, Recipe, UserRecipe

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
            user_recipes = UserRecipe.objects.filter(date=date, subscription_id=subscription.id)
            if not user_recipes:
                for subscription_meal_type in subscription.subscription_meal_types.all():
                    print(subscription_meal_type)
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

