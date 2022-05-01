import json
import os
import ssl
from django.http import HttpResponse
from django.shortcuts import redirect, render
from authentication.models import CustomUser
from authentication.forms import UserRegistrationForm
from django.contrib import messages
from django.contrib import auth
import requests
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site

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
            custom_user = CustomUser.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, birth_date=birth_date, password=password)
            custom_user.save()

            print('succeed')

            # Notification
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
        # print(user)
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
                return redirect("rent:home")
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


def password_reset(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "authentication/password_reset_email.txt"
                    current_site = get_current_site(request)
                    c = {
                        "email": user.email,
                        'domain': current_site,
                        'site_name': 'Car Rental App',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http', }

                    email = render_to_string(email_template_name, c)
                    message = EmailMessage(subject, email, to=[user.email])
                    message.send()
                    
            return redirect("auth:password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request, "authentication/password_reset.html", context={"password_reset_form": password_reset_form})


def password_reset_done(request):
    return render(request, "authentication/password_reset_done.html")


def password_reset_confirm(request, uidb64, token):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            uid = urlsafe_base64_decode(uidb64).decode()
            print(uid)
            user = CustomUser.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Votre Mot de passe a été modifié avec succes")
            return redirect("auth:password_reset_complete")
        else:
            messages.error(request, "Mots de Passe non identique")
              
        
        # messages.success(request, 'Votre lien a expiré')
        # return redirect("helpdesk:login")
        # associated_user = CustomUser.objects.filter(Q(email=data))

    return render(request, "authentication/password_reset_confirm.html")


def password_reset_complete(request):
    return render(request, "authentication/password_reset_complete.html")


@login_required(login_url="auth:login")
def home(request):
    return render(request, "authentication/home.html")
