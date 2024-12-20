from django.contrib import admin
from .models import Aircraft, Part

admin.site.register(Aircraft)
admin.site.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'aircraft', 'quantity', 'team')
