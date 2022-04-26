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
from turtle import home
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from CarRentalApp import settings
from authentication.views import login,signup 
from rentmodule import views
urlpatterns = [
    path('admin-panel/', admin.site.urls),
    
    path('', include('authentication.urls', namespace='auth')),path('admin/', admin.site.urls),
    
    path('car/', views.index, name='index'),
    path('car/car_detail/<int:pk>/', views.car_detail, name='car_detail'),
    path('car/edit/<int:pk>/', views.edit, name='edit'),
    path('car/create/', views.create, name='create'),
    path('car/delete/<int:pk>/', views.delete, name='delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
