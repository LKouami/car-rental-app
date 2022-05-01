from asyncio.windows_events import NULL
import uuid
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from authentication.models import CustomUser

CAR_STATE = (
    ("Libre", "Libre"),
    ("Réservée", "Réservée"),
    ("En réparation", "En réparation"),
)
RESERVATION_STATE = (
    ("En attente", "En attente"),
    ("En cours", "En cours"),
    ("Terminée", "Terminée"),
)

# Create your models here.

class Car(models.Model):
    brand = models.CharField(max_length=50, blank=False)
    modele = models.CharField(max_length=50, blank=False, default="")
    slug = models.SlugField(blank=True)
    color = models.CharField(max_length=30, blank=False)
    year = models.IntegerField()
    door = models.IntegerField()
    energy = models.CharField(max_length=25, blank=False)
    air_conditionner = models.BooleanField()
    state = models.CharField(max_length=25, blank=False, choices=CAR_STATE, default="Libre")
    price = models.FloatField(blank=False, default=0)
    default_picture = models.ImageField(upload_to='car_default_images')
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.brand)
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def __str__(self):
        return self.brand
    
    def get_absolute_url(self):
        return reverse("rent:car_details",
                        args=[self.id])
    
class CarImages(models.Model):
    name = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_images')
    default = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        # if CarImages.objects.filter(default = True).exists:
        #     print('This car already have default image')
        # else:
        if not self.slug:
            self.slug = slugify(self.name )
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "CarImage"
        verbose_name_plural = "CarImages"

    
class Reservation(models.Model):
    begin_date_time = models.DateTimeField(blank=False)
    end_date_time = models.DateTimeField(blank=False)
    state = models.CharField(max_length=25, blank=False, choices=RESERVATION_STATE, default="En attente")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True )
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"

class Bill(models.Model):
    number = models.CharField(max_length=50, blank=True)
    date_of_bill = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True )
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True )
    
    def save(self, *args, **kwargs):
        if not self.number:
            self.number =str(uuid.uuid4()) 
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Bill"
        verbose_name_plural = "Bills"

    def __str__(self):
        return self.number
    

    