from conf.wsgi import *

import datetime
import random

from foodplan.models import Subscription, SubscriptionMealType, Recipe, UserRecipe

active_subscriptions = Subscription.objects.filter(
        end_date__gte=datetime.date.today()
    )
subscription_meal_types = SubscriptionMealType.objects.filter(subscription__in=active_subscriptions)

date = datetime.date.today()

if __name__ == '__main__':
    for subscription_meal_type in subscription_meal_types:
        subscription = subscription_meal_type.subscription
        meal_type = subscription_meal_type.meal_type
        menu_type = subscription.menu_type
        allergies = subscription.allergies.all()
        user_dislike_recipes = UserRecipe.objects.filter(user=subscription.user, reaction='dislike').values_list('recipe__pk', flat=True)
        print(user_dislike_recipes)
        possible_recipes = Recipe.objects.filter(
            menu_type=menu_type,
            meal_type=meal_type,
        ).exclude(
            ingredients__allergy__in=allergies,
        ).exclude(
            pk__in=user_dislike_recipes,
        )
        random_recipe = random.choice(possible_recipes)
        print(f'Possible recipes for {subscription.user} with {meal_type} meal type: {random_recipe}')
