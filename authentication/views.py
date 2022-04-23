from turtle import home
from django.http import HttpResponse
from django.shortcuts import redirect, render
from authentication.models import CustomUser
from authentication.forms import UserRegistrationForm
from django.contrib import messages
from django.contrib import auth
import requests
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('je rentre ici')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            birth_date = form.cleaned_data['birth_date']
            password = form.cleaned_data['password']           
            custom_user = CustomUser.objects.create_user( first_name=first_name, last_name=last_name, email=email, birth_date=birth_date, password=password)
            custom_user.save()

            print('succeed')
            
            #Notification
            messages.success(request, "Inscription réussie.")
            return redirect("auth:login")
        else:
            # print(form.cleaned_data['password'])
            # print(form.cleaned_data['confirm_password'])
            # print(form.errors)
            print(form.is_valid())

    else:
        print('eroooor2222')
        form = UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, "authentication/signup.html", context)

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)
        #print(user)
        if user is not None:
            auth.login(request, user)
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect("auth:home")
        else:
            messages.error(request, "Identifiant incorrect.")
            return render(request, "authentication/login.html")

    return render(request, "authentication/login.html")

@login_required(login_url="auth:login")
def logout(request):
    auth.logout(request)
    return redirect("auth:login")

def password_forgot(request):
    return render(request, "authentication/signup.html")

@login_required(login_url="auth:login")
def home(request):
    return render(request, "authentication/home.html")
