"""Car Commands"""

import pickle
import pandas as pd
from surprise import Dataset, Reader, SVD

# Django
from django.core.management.base import BaseCommand

# Models
from app_django.cars.models import Rating

class Command(BaseCommand):
    help = 'Train SVD model using surprise'

    def handle(self, *args, **kwargs):
        
        try:
            ratings = [(rating.user.id, rating.car.id, rating.rating) for rating in Rating.objects.all()]
            df_ratings = pd.DataFrame(ratings, columns=['user_id', 'car_id', 'rating'])
            reader = Reader(rating_scale=(1, 5))
            data = Dataset.load_from_df(df_ratings[['user_id', 'car_id', 'rating']], reader)
            trainset = data.build_full_trainset()
            model = SVD()
            model.fit(trainset)
            with open('app_django/cars/pickle_files/modelo_svd.pkl', 'wb') as file:
                pickle.dump(model, file)

            self.stdout.write(self.style.SUCCESS('Model saved successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading data: {e}'))