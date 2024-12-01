# Python
from typing import Any

# Recommender system libraries
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from surprise import Dataset, Reader, SVD


def recommend_cars(auto_id: int, autos_encoded: pd.DataFrame, similaridades, top_n=4):
    # Obtener el índice del auto en autos_encoded
    idx = autos_encoded.index.get_loc(auto_id)
    # Obtener las similitudes del auto dado con todos los demás autos
    simil_auto = similaridades[idx]
    # Ordenar las similitudes y obtener los índices de los autos más similares
    similar_idx = np.argsort(-simil_auto)[1:top_n+1]
    # Devolver los IDs de los autos recomendados
    return list(autos_encoded.index[similar_idx])


def get_recommended_car_ids(cars_list: list[dict[str, Any]], car_id: int):
    """
    Get recommended car IDs using cosine similarity.

    This function calculates cosine similarity to recommend car IDs based on a given car ID and a list of cars.

    Args:
        cars_list (list of dict): A list where each element is a dictionary representing a car, with features used for similarity calculation.
        car_id (int or str): The ID of the current car displayed on the webpage.

    Returns:
        list: A list of recommended car IDs based on cosine similarity.
    """
    cars_df = pd.DataFrame(cars_list)
    numeric_columns = ['price', 'year', 'km', 'cilinder', 'engine']
    cars_df[numeric_columns] = cars_df[numeric_columns].astype(float)
    cars_df.drop(columns=['created','modified','is_active', 'urlpic', 'currency'], inplace=True)
    cars_df.set_index('id', inplace=True)

    categorical_columns = ['brand', 'model', 'version', 'fuel_type', 'transmission', 'location', 'color', 'upholstery']
    # Perform target encoding
    for col in categorical_columns:
        # Calculate the mean of the target variable for each category
        mean_target = cars_df.groupby(col)['price'].mean()
        # Replace each category with its corresponding mean value
        cars_df[col] = cars_df[col].map(mean_target)
    
    cars_df = cars_df.fillna(0)
    similarities = cosine_similarity(cars_df)
    recommended_car_ids = recommend_cars(car_id, cars_df, similarities)
    return recommended_car_ids


def get_predictions_surprise(ratings: list[tuple[int,int,int]], user_id: int, top_n: int = 4) -> list[int]:
    """
    Train a recommendation model using the Surprise library and return the top N items
    with the highest predicted rating for a specific user.

    Args:
        ratings (list of tuple): A list containing tuples with the following structure:
            - user_id (int): The ID of the user.
            - car_id (int): The ID of the item (car).
            - rating (float): The rating given by the user to the item.
        user_id (int): The current user ID for whom to retrieve recommendations.
        top_n (int, optional): The number of top recommendations to return. Default is 4.

    Returns:
        list[int]: A list of item IDs (car IDs) representing the top N recommended items for the specified user,
                   sorted by the predicted rating in descending order.
    """
    df_ratings = pd.DataFrame(ratings, columns=['user_id', 'car_id', 'rating'])
    
    # Train SVD model using surprise
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df_ratings[['user_id', 'car_id', 'rating']], reader)
    trainset = data.build_full_trainset()
    model = SVD(n_factors=100, n_epochs=20)
    model.fit(trainset)

    # Get predictions from trained model
    rated_items = df_ratings[df_ratings['user_id'] == user_id]['car_id'].tolist()
    unique_items = df_ratings['car_id'].unique()
    items_to_predict = [item for item in unique_items if item not in rated_items]
    predictions = model.test([(user_id, item, 0) for item in items_to_predict])
    top_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)[:top_n]
    top_item_ids = [prediction.iid for prediction in top_predictions]
    return top_item_ids