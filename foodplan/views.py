import datetime

from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Subscription, MenuType, MealType, Allergy

# Create your views here.
def index(request):
    return render(request,
                  'foodplan/index.html',
                  )


@login_required
def lk(request):
    active_subscriptions = request.user.subscriptions.filter(
        end_date__gte=datetime.date.today()
    )

    return render(request, 'foodplan/lk.html',
                  context={
                      'active_subscriptions': active_subscriptions,
                      'username': request.user.username,
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
    persons = int(request.GET.get('select5', '1'))      # кол-во человек

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
