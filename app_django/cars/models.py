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
    price = models.CharField(max_length=20)  # Adjusted to CharField to handle different price formats
    urlpic = models.URLField(max_length=255)
    year = models.PositiveIntegerField()
    km = models.CharField(max_length=20)  # Adjusted to CharField to handle "17000 km" format
    gastype = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    location = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)



