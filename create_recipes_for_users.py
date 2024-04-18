from conf.wsgi import *

import datetime

from foodplan.models import Subscription, SubscriptionMealType, Recipe

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
        possible_recipes = Recipe.objects.filter(
            menu_type=menu_type,
            meal_type=meal_type,
        ).exclude(
            ingredients__allergy__in=allergies
        )
        print(f'Possible recipes for {subscription.user} with {meal_type} meal type: {possible_recipes}')
