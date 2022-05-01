from django.contrib import admin
from rentmodule.models import Bill, Car, CarImages, Reservation
from django.contrib import admin
from authentication.models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
import csv
import datetime
# Register your models here.


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many\
    and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'



@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand','modele', 'color', 'year','door', 'energy', 'air_conditionner', 'state','price','default_picture')
    list_filter = ('brand','modele', 'color', 'year','door', 'energy', 'air_conditionner', 'state','price')
    list_per_page = 20
    fieldsets = (
        ('None', {'fields': ('brand', 'modele', 'color', 'year','door', 'energy', 'air_conditionner', 'state','price', 'default_picture')}),
    )
    actions = [export_to_csv]
    
@admin.register(CarImages)
class CarImagesAdmin(admin.ModelAdmin):
    list_display = ('name', 'car', 'image','default')
    list_filter = ('name', 'car','default')
    list_per_page = 20
    fieldsets = (
        ('None', {'fields': ('name', 'car', 'image','default')}),
    )
    actions = [export_to_csv]

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('begin_date_time', 'end_date_time', 'state','car','client')
    list_filter = ( 'state','car','client')
    list_per_page = 20
    fieldsets = (
        ('None', {'fields': ('begin_date_time', 'end_date_time', 'state','car','client')}),
    )
    actions = [export_to_csv]

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('number', 'date_of_bill', 'client','car','reservation')
    list_filter = ( 'date_of_bill', 'client','car','reservation')
    list_per_page = 20
    fieldsets = (
        ('None', {'fields': ('number', 'client','car','reservation')}),
    )
    actions = [export_to_csv]
    


admin.site.site_header = "CAR RENTAL ADMIN"
admin.site.site_title = "CAR RENTAL ADMIN"