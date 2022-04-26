from django.db import models

# Create your models here.
class Car(models.Model):
    brand=models.CharField(max_length=50)
    color=models.CharField(max_length=50)
    year=models.CharField(max_length=50)
    door=models.CharField(max_length=50)
    energy=models.CharField(max_length=50)
    air_conditionner=models.BooleanField(default=False)
    picture=models.ImageField(upload_to="cars", blank=True, null=True,max_length=50)
    state=models.CharField(max_length=50)
    
    def __str__(self):
        return self.brand
    
class Customer(models.Model):
    first_name=models.CharField(max_length=50, blank=False, default="")
    name=models.CharField(max_length=50, blank=False, default="")
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    birthday=models.DateTimeField(auto_now_add=True,null=True)
    sexe=models.CharField(max_length=50)
    credible=models.BooleanField(default=False)
    tel=models.CharField(max_length=50)
    cni_num=models.CharField(max_length=50)
    dlicense_num=models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name} {self.first_name}"


class Reservation(models.Model):
    car=models.ForeignKey(Car,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    begin_date=models.CharField(max_length=50)
    begin_hour=models.CharField(max_length=50)
    end_date=models.CharField(max_length=50)
    end_hour=models.CharField(max_length=50)
    
    def __str_(self):
        return f"{self.begin_date} {self.end_date}"
    
class Bill(models.Model):
    reservation=models.ForeignKey(Reservation,on_delete=models.CASCADE)
    price=models.IntegerField(null=True)
    date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    def __str__(self):
        return self.price