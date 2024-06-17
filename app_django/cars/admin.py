"""Car admin."""

# Django
from django.contrib import admin

# Models
from app_django.cars.models import Car

@admin.register(Car)
class ProductAdmin(admin.ModelAdmin):
    """Car admin."""

    list_display = ('id', 'brand', 'model', 'version', 'is_active', 'created', 'modified')
    list_display_links = ('id',)
    
    search_fields = ('brand', 'is_active')
    
    list_filter = ('created', 'modified')

