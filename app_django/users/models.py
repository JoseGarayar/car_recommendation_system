"""User model"""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Utilities
from app_django.utils.models import BaseAppModel


class UserManager(BaseUserManager):
    """User model.

    Force to add an email when creating a superuser.
    """
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Ingresa un email')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(BaseAppModel, AbstractUser):
    """User model.

    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []