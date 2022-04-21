from django.shortcuts import render

# Create your views here.

def signup(request):
    return render(request, "authentication/signup.html")

def login(request):
    return render(request, "authentication/login.html")

def password_forgot(request):
    return render(request, "authentication/signup.html")
