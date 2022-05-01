from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from collections import namedtuple
from rentmodule.models import Car, CarImages
from django.contrib.auth.decorators import login_required

# Create your views here.
    
@login_required(login_url="auth:login")
def home(request):
    return render(request, "rent/home.html")

@login_required(login_url="auth:login")
def locations_list(request):
    return render(request, "rent/my_locations.html")

@login_required(login_url="auth:login")
def about(request):
    return render(request, "rent/about.html")

@login_required(login_url="auth:login")
def cars_detail(request, car_id):
    print(request.user)
    print('Je viens ici')
    car_detail = get_object_or_404(Car,  id=car_id)
    print(car_detail)
    context = {
        "car_detail": car_detail,
    }
    print(car_id)
    return render(request, "rent/my_cars_details.html", context)

@login_required(login_url="auth:login")
def cars_list(request):
    cars = Car.objects.order_by('-brand')
    paginator = Paginator(cars, 8)
    page = request.GET.get('page')
    try:
        total = paginator.num_pages
        cars = paginator.page(page)
    except PageNotAnInteger:
        cars = paginator.page(1)
    except EmptyPage:
        cars = paginator.page(paginator.num_pages)
    context = {
        "cars": cars,
        "total": total
    }
    return render(request, "rent/my_cars.html", context=context)