from tabnanny import verbose
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=36)
    slug = models.SlugField(blank=True)
    @property
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Car(models.Model):
    author = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    category = models.ManyToManyField(Category)
    brand = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    color = models.CharField(max_length=100)
    door = models.CharField(max_length=2)
    energy = models.CharField(max_length=20)
    picture = models.CharField(max_length=100)
    Year = models.DateField(blank=True, null=True)
    description = models.TextField()
    air_conditionner = models.BooleanField(default=False)
    availaible = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Voiture"

    def __str__(self):
        return self.brand
        
    @property
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.brand)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return " "