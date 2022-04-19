from django.contrib import admin

# Register your models here.
from rentmodule.models import Car, Category

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    List_display = (
        "author",
        "brand",
        "slug"
    )