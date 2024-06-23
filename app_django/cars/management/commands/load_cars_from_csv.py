"""Car Commands"""

import csv
from django.core.management.base import BaseCommand
from app_django.cars.models import Car

class Command(BaseCommand):
    help = 'Load car data from a CSV file into the Car model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to be loaded')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        
        try:
            with open(csv_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    km_value = int(row['KM'].replace(',', ''))
                    price_value = float(row['Price'])
                    cilinder_value = float(row['Cilinder']) if row['Cilinder'] else None
                    engine_value = float(row['Engine']) if row['Engine'] else None
                    age_value = int(row['Age'])
                    
                    car = Car(
                        brand=row['Brands'],
                        model=row['Models'],
                        version=row['Version'],
                        currency=row['Currency'],
                        price=price_value,
                        urlpic=row['Urlpic'],
                        year=int(row['Year']),
                        km=km_value,
                        fuel_type=row['Fuel_type'],
                        transmission=row['Transmission'],
                        location=row['Location'],
                        color=row['Color'],
                        cilinder=cilinder_value,
                        upholstery=row['Upholstery'],
                        engine=engine_value,
                        age=age_value,
                        is_active=True
                    )
                    car.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully loaded data from {csv_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading data: {e}'))