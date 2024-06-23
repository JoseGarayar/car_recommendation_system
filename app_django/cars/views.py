"""Cars views."""

# Django
from django.views.generic import ListView, TemplateView, DetailView
from django.db.models import Q

# Models
from app_django.cars.models import Car

# Helper functions
from app_django.cars.functions import recommend_cars

# Recommendation system
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class HomeView(ListView):
    """Homepage view."""

    template_name = 'home.html'
    model = Car
    ordering = ('-created',)
    paginate_by = 4
    context_object_name = 'cars'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class StoreView(ListView):
    """Return all cars."""

    template_name = 'cars/store.html'
    model = Car
    ordering = ('id',)
    paginate_by = 12
    context_object_name = 'cars'


class CarDetailView(DetailView):
    """Return detail for a single car."""

    template_name = 'cars/detail_car.html'
    queryset = Car.objects.all()
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        cars = self.get_queryset()
        cars_list = list(cars.values())
        cars_df = pd.DataFrame(cars_list)
        numeric_columns = ['price', 'year', 'km', 'cilinder', 'engine', 'age']
        cars_df[numeric_columns] = cars_df[numeric_columns].astype(float)
        cars_df.drop(columns=['created','modified','is_active', 'urlpic'], inplace=True)
        cars_encoded = pd.get_dummies(cars_df.set_index('id'))
        
        # Normalizar los precios para que las magnitudes no dominen la similitud
        if 'price' in cars_df.columns:
            cars_df['price'] = (cars_df['price'] - cars_df['price'].min()) / (cars_df['price'].max() - cars_df['price'].min())
        
        similarities = cosine_similarity(cars_df)
        car_id = context['car'].id
        recommendations = recommend_cars(car_id, cars_df, similarities)
        car_recommendations = Car.objects.filter(pk__in=recommendations)
        context['car_recommendations'] = car_recommendations

        return context