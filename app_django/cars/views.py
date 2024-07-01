"""Cars views."""

# Django
from django.views.generic import ListView, TemplateView, DetailView

# Models
from app_django.cars.models import Car

# Helper functions
from app_django.cars.functions import recommend_cars

# Forms
from app_django.cars.forms import CarPriceForm

# Recommendation system
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle


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
        cars_df.drop(columns=['created','modified','is_active', 'urlpic', 'currency'], inplace=True)
        cars_df.set_index('id', inplace=True)

        # cars_encoded = pd.get_dummies(cars_df.set_index('id'))
        categorical_columns = ['brand', 'model', 'version', 'fuel_type', 'transmission', 'location', 'color', 'upholstery']
        # Perform target encoding
        for col in categorical_columns:
            # Calculate the mean of the target variable for each category
            mean_target = cars_df.groupby(col)['price'].mean()
            # Replace each category with its corresponding mean value
            cars_df[col] = cars_df[col].map(mean_target)
        # Normalizar los precios para que las magnitudes no dominen la similitud
        if 'price' in cars_df.columns:
            cars_df['price'] = (cars_df['price'] - cars_df['price'].min()) / (cars_df['price'].max() - cars_df['price'].min())
        
        print(cars_df.columns.to_list())
        cars_df = cars_df.fillna(0)
        similarities = cosine_similarity(cars_df)
        car_id = context['car'].id
        recommendations = recommend_cars(car_id, cars_df, similarities)
        print(recommendations)
        car_recommendations = Car.objects.filter(pk__in=recommendations)
        print(car_recommendations)
        context['car_recommendations'] = car_recommendations

        return context
    

class CarPriceEstimatorView(TemplateView):
    """Return car price estimate."""

    template_name = 'cars/car_price_estimator.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CarPriceForm(self.request.GET or None)
        context['form'] = form

        if form.is_valid():
            data = form.cleaned_data

            # Import model
            with open(f'app_model/objects/encoder.pkl', 'rb') as file:
                encoder = pickle.load(file)

            with open(f'app_model/objects/transformer.pkl', 'rb') as file:
                transformer = pickle.load(file)

            with open(f'app_model/objects/estimator.pkl', 'rb') as file:
                estimator = pickle.load(file)
            
            features = [
                2024 - data['year'], data['brand'], float(data['cilinder']), data['color'],
                float(data['engine']), data['fuel_type'], data['km'], data['location'],
                data['model'], data['transmission'], data['upholstery'], data['version']
            ]
            print(features)
            print('encoder', encoder)
            print('transformer', transformer)
            print('estimator', estimator)
            
            keys = estimator.get_booster().feature_names
            sample = pd.DataFrame(dict(zip(keys, [[v] for v in features])))
            sample = encoder.transform(sample)
            sample = transformer.transform(sample)
            price = estimator.predict(sample)[0]

            context['result'] = price
        else:
            context['result'] = None

        return context
        
