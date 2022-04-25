from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, birth_date, password=None, **extra_fields):
        if not email:
            raise ValueError("Vous devez entrer une adresse mail")
        if not first_name:
            raise ValueError("Vous devez entrer un prénom")
        if not last_name:
            raise ValueError("Vous devez entrer un nom")
        if not birth_date:
            raise ValueError("Vous devez entrer une date de naissance")
        user = self.model(
            email = self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name, last_name, birth_date, password=None):
        user=self.create_user(email=email, first_name=first_name, last_name=last_name, password=password, birth_date = birth_date)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False
    )
    first_name = models.CharField(max_length=50, blank=True, default="")
    last_name = models.CharField(max_length=50, blank=True, default="")
    birth_date = models.DateField(blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["birth_date","first_name", "last_name"]
    objects = MyUserManager()
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"