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
app_name = "auth"
urlpatterns = [
    path('auth/password_reset',views.password_reset, name='password_reset'),
    path('auth/password_reset_confirm/<uidb64>/<token>/',views.password_reset_confirm, name='password_reset_confirm'),
    path('auth/password_reset_complete',views.password_reset_complete, name='password_reset_complete'),
    path('auth/password_reset_done',views.password_reset_done, name='password_reset_done'),
    path('auth/login/',views.login, name='login'),
    path('auth/signup/',views.signup, name='signup'),
    path('logout/', views.logout, name="logout"),
    
]
