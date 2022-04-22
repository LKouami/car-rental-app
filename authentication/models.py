from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, birth_date, password=None):
        if not email:
            raise ValueError("You should enter an email")
        user = self.model(
            email = self.normalize_email(email)
        )
        user.birth_date= birth_date
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, birth_date, password=None):
        user=self.create_user(email=email, password=password, birth_date = birth_date)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    birth_date = models.DateField(blank=False, default= datetime.now())
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["birth_date"]
    objects = MyUserManager()
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True