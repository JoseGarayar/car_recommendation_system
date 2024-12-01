"""Car Commands"""

import pickle
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import cross_validate

# Django
from django.core.management.base import BaseCommand

# Models
from app_django.cars.models import Rating

class Command(BaseCommand):
    help = 'Run 5-fold cross-validation for SVD model and print results'

    def handle(self, *args, **kwargs):
        
        try:
            ratings = list(Rating.objects.select_related('user', 'car').values_list('user_id', 'car_id', 'rating'))
            df_ratings = pd.DataFrame(ratings, columns=['user_id', 'car_id', 'rating'])
            reader = Reader(rating_scale=(1, 5))
            data = Dataset.load_from_df(df_ratings[['user_id', 'car_id', 'rating']], reader)
            model = SVD(n_factors=100, n_epochs=20)
            cross_validate(model, data, measures=['RMSE', 'MAE'], cv=5, verbose=True, return_train_measures=True)
            self.stdout.write(self.style.SUCCESS('Run successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading data: {e}'))