"""Car Commands"""

import pickle
import pandas as pd
from pathlib import Path
from surprise import Dataset, Reader, SVD
from surprise.model_selection import GridSearchCV

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
            param_grid = {"n_epochs": [5, 10], "lr_all": [0.002, 0.005], "reg_all": [0.4, 0.6]}
            gs = GridSearchCV(SVD, param_grid, measures=["rmse", "mae"], cv=5, return_train_measures=True)
            gs.fit(data)
            # best RMSE score
            print(gs.best_score["rmse"])
            # combination of parameters that gave the best RMSE score
            print(gs.best_params["rmse"])
            # algorithm with the best rmse
            algo = gs.best_estimator["rmse"]
            # Train algorithm
            algo.fit(data.build_full_trainset())
            # Create all directories for surprise model path
            surprise_model_path = Path("app_django/cars/surprise_model/svd.pkl")
            surprise_model_path.parent.mkdir(parents=True, exist_ok=True)
            with open(surprise_model_path, 'wb') as file:
                pickle.dump(algo, file)
            # Get dataframe with all the needed information
            results_df = pd.DataFrame.from_dict(gs.cv_results)
            # Save dataframe in a csv file
            csv_path = Path("app_django/cars/media/results.csv")
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            with open(csv_path, mode='w', encoding='utf-8') as archivo:
                results_df.to_csv(archivo, index=False)
            self.stdout.write(self.style.SUCCESS('CSV file saved successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading data: {e}'))