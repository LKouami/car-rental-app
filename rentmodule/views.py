from django.shortcuts import render, get_object_or_404, redirect

from rentmodule.models import Car
from .forms import CarForm
# Create your views here.

def index(request):
    cars = Car.objects.all()
    return render(request, 'car/index.html', context={"cars": cars})

def car_detail(request, brand):
    car = get_object_or_404(Car, brand=brand)
    return render(request, 'car/detail.html', context={"car": car})

def create(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    form = CarForm()

    return render(request,'car/create.html',{'form': form})

def edit(request, pk, template_name='car/edit.html'):
    car = get_object_or_404(Car, pk=pk)
    form = CarForm(request.POST or None, instance=car)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, template_name, {'form':form})

def delete(request, pk, template_name='car/delete.html'):
    car = get_object_or_404(Car, pk=pk)
    if request.method=='POST':
        car.delete()
        return redirect('index')
    return render(request, template_name, {'object':car})