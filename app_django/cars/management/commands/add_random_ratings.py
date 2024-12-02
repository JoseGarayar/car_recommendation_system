"""Car Commands"""

import random
from django.core.management.base import BaseCommand
from app_django.cars.functions import get_recommended_car_ids
from app_django.cars.models import Car, Rating
from app_django.users.models import User

class Command(BaseCommand):
    help = 'Add random ratings to all users'

    def handle(self, *args, **kwargs):
        try:
            users = User.objects.all().values()
            cars = list(Car.objects.all().values())
            ratings_list = (1,2,3,4,5)
            num_ratings_per_user = 15
            for user in users:
                random_car_id = random.choice(cars)['id']
                set_car_ids = set()
                set_car_ids.add(random_car_id)
                for _ in range(num_ratings_per_user):
                    rating_value = random.choice(ratings_list)
                    recommended_car_ids = get_recommended_car_ids(cars, random_car_id)
                    random_car_id = random.choice(recommended_car_ids)
                    set_car_ids.add(random_car_id)
                list_rating_instances = [Rating(
                                            user_id=user['id'],
                                            car_id=car_id,
                                            rating= rating_value
                                        ) for car_id in set_car_ids]
                Rating.objects.bulk_create(list_rating_instances)
                
                self.stdout.write(self.style.SUCCESS(f'Successfully added rating data for user: {user["id"]}'))

            self.stdout.write(self.style.SUCCESS(f'Successfully added rating data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading data: {e}'))