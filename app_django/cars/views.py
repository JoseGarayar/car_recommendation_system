"""Cars views."""

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, DetailView

# Models
from app_django.cars.models import Car, Rating

# Helper functions
from app_django.cars.functions import get_recommended_car_ids, get_predictions_surprise

# Forms
from app_django.cars.forms import CarPriceForm

# Recommendation system
import pandas as pd
import pickle
import json

# Utils
from app_django.utils.mixins import CustomLoginRequiredMixin


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


class StoreView(CustomLoginRequiredMixin, ListView):
    """Return all cars."""

    template_name = 'cars/store.html'
    model = Car
    ordering = ('id',)
    paginate_by = 12
    context_object_name = 'cars'

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = []
        brand = self.request.GET.get("brand")
        model = self.request.GET.get("model")
        if brand:
            filters.append(Q(brand=brand))
        if model:
            filters.append(Q(model=model))
        return queryset.filter(*filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        with open('app_model/json_files/brand_model.json', 'r') as file:
            brand_model_data = json.load(file)

        context['brand_model_data'] = brand_model_data
        return context


class CarDetailView(CustomLoginRequiredMixin, DetailView):
    """Return detail for a single car."""

    template_name = 'cars/detail_car.html'
    queryset = Car.objects.all()
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Recommender system
        cars = self.get_queryset()
        cars_list = list(cars.values())
        recommended_car_ids = get_recommended_car_ids(cars_list, context['car'].id)
        car_recommendations = Car.objects.filter(pk__in=recommended_car_ids)
        context['car_recommendations'] = car_recommendations

        # Recommender system using surprise
        ratings = [(rating.user.id, rating.car.id, rating.rating) for rating in Rating.objects.all()]
        df_ratings = pd.DataFrame(ratings, columns=['user_id', 'car_id', 'rating'])
        top_cars_ids = get_predictions_surprise(df_ratings, self.request.user.id)
        top_cars = Car.objects.filter(pk__in=top_cars_ids)
        context['top_cars_svd'] = top_cars

        # Add ratings
        user_rating = Rating.objects.filter(user=self.request.user, car=self.object).first()
        context['user_rating'] = user_rating.rating if user_rating else None

        return context
    

class CarPriceEstimatorView(CustomLoginRequiredMixin, TemplateView):
    """Return car price estimate."""

    template_name = 'cars/car_price_estimator.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        with open('app_model/json_files/brand_model.json', 'r') as file:
            brand_model_data = json.load(file)
        with open('app_model/json_files/unique_cat_values.json', 'r') as file:
            unique_cat_values = json.load(file)

        form = CarPriceForm(self.request.GET or None)
        context['form'] = form
        context['brand_model_data'] = brand_model_data
        context['colors'] = unique_cat_values['Color']
        context['transmissions'] = unique_cat_values['Transmission']
        context['versions'] = unique_cat_values['Version']
        context['fuel_types'] = unique_cat_values['Fuel_type']
        context['locations'] = unique_cat_values['Location']
        context['upholstery'] = unique_cat_values['Upholstery']

        if form.is_valid():
            data = form.cleaned_data

            # Import model
            with open(f'app_model/objects/encoder.pkl', 'rb') as file:
                encoder = pickle.load(file)
            with open(f'app_model/objects/transformer.pkl', 'rb') as file:
                transformer = pickle.load(file)
            with open(f'app_model/objects/estimator.pkl', 'rb') as file:
                estimator = pickle.load(file)
            with open(f'app_model/objects/calibrator.pkl', 'rb') as file:
                calibrator = pickle.load(file)
            
            current_year = 2024
            car_age = data['year']
            age = current_year - car_age
            features = [
                age, data['brand'], float(data['cilinder']), data['color'],
                float(data['engine']), data['fuel_type'], data['km'], data['location'],
                data['model'], data['transmission'], data['upholstery'], data['version']
            ]
            
            keys = estimator.get_booster().feature_names
            sample = pd.DataFrame(dict(zip(keys, [[v] for v in features])))
            sample = encoder.transform(sample)
            sample = transformer.transform(sample)
            price = estimator.predict(sample)[0]
            vector_cal = [price, car_age]
            keys = calibrator.get_booster().feature_names
            sample = pd.DataFrame(dict(zip(keys, [[v] for v in vector_cal])))
            price_cal = calibrator.predict(sample)[0]

            context['result'] = price_cal
        else:
            context['result'] = None

        return context
        

@login_required
def rate_car(request, car_id):
    if request.method == 'POST':
        car = get_object_or_404(Car, id=car_id)
        rating_value = int(request.POST.get('rating', 0))

        if 0 < rating_value <= 5:
            Rating.objects.update_or_create(
                user=request.user,
                car=car,
                defaults={'rating': rating_value},
            )
            messages.success(request, "Tu calificación ha sido enviada correctamente!")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        messages.error(request, "Error en calificación enviada!")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    messages.error(request, "El método de solicitud no es válido!")
    return redirect(request.META.get('HTTP_REFERER', '/'))