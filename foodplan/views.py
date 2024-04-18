from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,
                  'foodplan/index.html',
                  )

def lk(request):
    return render(request,
                  'foodplan/lk.html',
                  )
