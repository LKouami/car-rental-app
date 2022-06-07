"""CarRentalApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from CarRentalApp import settings
from django.conf.urls.static import static
app_name = "rent"
urlpatterns = [
    
    path('',views.home, name='home'),
    path('cars_list',views.cars_list, name='cars_list'),
    path('cars_detail/<int:car_id>/',views.cars_detail, name='cars_detail'),
    path('reservation_actions/<int:car_id>/',views.reservation_actions, name='reservation_actions'),
    path('locations_list',views.locations_list, name='locations_list'),
    path('download_bill/<int:reservation_id>/',views.billgen, name='billgen'),
    path('about',views.about, name='about'),
    
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
