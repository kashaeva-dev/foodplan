import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
