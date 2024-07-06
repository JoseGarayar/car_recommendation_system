"""Cars models."""

# Django
from django.db import models

# Utilities
from app_django.utils.models import BaseAppModel


class Car(BaseAppModel):
    """Car model."""
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    version = models.CharField(max_length=100)
    currency = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    urlpic = models.URLField(max_length=255)
    year = models.PositiveIntegerField(null=True, blank=True)
    km = models.PositiveIntegerField(null=True, blank=True)
    fuel_type = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    color = models.CharField(max_length=50, null=True, blank=True)
    cilinder = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    upholstery = models.CharField(max_length=50, null=True, blank=True)
    engine = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    is_active = models.BooleanField(default=True)



