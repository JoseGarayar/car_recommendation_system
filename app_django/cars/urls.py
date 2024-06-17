"""Productos URLs."""

# Django
from django.urls import path

# Views
from cars import views

urlpatterns = [

    path(
        route='',
        view=views.HomeView.as_view(),
        name='home'
    ),

    path(
        route='store/',
        view=views.StoreView.as_view(),
        name='store'
    ),

    path(
        route='car/<int:pk>',
        view=views.CarDetailView.as_view(),
        name='detail'
    )
]