# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from app_django.users.models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'created', 'modified')