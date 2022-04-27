from django.db import models
from django.utils.text import slugify

CAR_STATE = (
    ("Libre", "Libre"),
    ("Réservé", "Réservé"),
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
    slug = models.SlugField(blank=True)
    color = models.CharField(max_length=30, blank=False)
    year = models.IntegerField()
    door = models.IntegerField()
    energy = models.CharField(max_length=25, blank=False)
    air_conditionner = models.BooleanField()
    state = models.CharField(max_length=25, blank=False, choices=CAR_STATE, default="Libre")
    price = models.FloatField(blank=False, default=0)
    @property
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.brand+self.pk)
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def __str__(self):
        return self.brand
    
class CarImages(models.Model):
    name = models.CharField(max_length=255, blank=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_images/')
    default = models.BooleanField(default=False)
    
class Reservation(models.Model):
    begin_date_time = models.DateTimeField(blank=False)
    end_date_time = models.DateTimeField(blank=False)
    state = models.CharField(max_length=25, blank=False, choices=RESERVATION_STATE, default="En attente")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True )

class Bill(models.Model):
    date_of_bill = models.DateTimeField(auto_now=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True )
    

    