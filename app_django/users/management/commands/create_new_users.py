"""User Commands"""

import csv
from django.core.management.base import BaseCommand
from app_django.users.models import User

class Command(BaseCommand):
    help = 'Create new users in the User model from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to be loaded')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        
        try:
            with open(csv_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                
                for row in reader:
                    username = row['Username']
                    email = row['Email']
                    password = row['Password']
                    
                    User.objects.create_user(
                        username=username,
                        email=email, 
                        password=password
                    )

            self.stdout.write(self.style.SUCCESS(f'Successfully loaded data from {csv_file}, total users: {User.objects.all().count()}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading data: {e}'))