from django.contrib import admin

from .models import motorcycle, detail


class MotorcycleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Date information', {'fields': ['pub_date']}),
        ('Brand', {'fields': ['brand']})
    ]

admin.site.register(motorcycle, MotorcycleAdmin)

admin.site.register(detail)