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

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'last_name', 'first_name','birth_date', 'sexe', 'cni_num', 'credible','dlicense_num', 'tel', 'last_login', 'date_joined', 'is_active')
    list_display_links = ['email']
    readonly_fields = ('last_login', 'date_joined')
    exclude = ('user_permissions', 'is_superuser', 'groups', 'username')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ['last_login', 'is_active']
    list_per_page = 20
    fieldsets = (
        ('Personal info', {'fields': ('email', 'last_name', 'first_name','birth_date', 'sexe', 'cni_num', 'credible','dlicense_num', 'tel', 'password')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin')}),
    )
    actions = [export_to_csv]