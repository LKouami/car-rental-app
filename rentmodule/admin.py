from django.contrib import admin
from rentmodule.models import Car,Customer,Reservation,Bill
# Register your models here.
admin.site.register(Car)
admin.site.register(Customer)
admin.site.register(Reservation)
admin.site.register(Bill)
