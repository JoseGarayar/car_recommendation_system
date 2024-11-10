"""Productos URLs."""

# Django
from django.urls import path

# Views
from users import views

urlpatterns = [

    path(
        route='login/',
        view=views.login_user,
        name='login'
    ),
    path(
        route='logout/',
        view=views.logout_user,
        name='logout'
    ),
    path(
        route='signup/',
        view=views.signup_user,
        name='signup'
    )
]