from django.core.management.base import BaseCommand, CommandError

from django.apps import apps

import csv

from django.db import DataError



######################################################################
# from dataentry.models import Student
# handle only one model
# Proposed command : python manage.py importdata file_path
# '''

# class Command(BaseCommand):
#     help = "Import data from CSV file"
    
#     def add_arguments(self, parser):
#         parser.add_argument('file_path', type=str, help='Path to the CSV file')
    
#     def handle(self, *args, **kwargs):
#         # Logic goes here
#         file_path = kwargs['file_path']
#         with open(file_path, 'r') as file:
#             reader = csv.DictReader(file)
#             # print(reader)
#             for row in reader:
#                 # print(row) : output = {'roll_no': '10050', 'name': 'James Turner', 'age': '19'}
#                 Student.objects.create(**row)
#         self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully!'))

# # "C:\Users\ogwue\OneDrive\Desktop\Datasets\student_data.csv"

# '''


######################################################################
# handle any model one model
# Proposed command : python manage.py importdata file_path model_name


class Command(BaseCommand):
    help = "Import data from CSV file"
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        parser.add_argument('model_name', type=str, help='Name of the model')
        
    def handle(self, *args, **kwargs):
        # Logic goes here
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()
        
        # Search for the model across all installed apps
        model = None
        for app_config in apps.get_app_configs():
            # Try to search for the model
            try:
                model = apps.get_model(app_config.label, model_name)
                break # stop searching once the model is found
            except LookupError:
                continue # model not found in this app, continue searching in the next app
        
        if not model:
            raise CommandError(f'Model "{model_name}" not found in any app!')
        
        
        
        # get all the field names of that model we found
        # Exclude the id field
        model_fields = [ field.name for field in model._meta.fields if field.name != 'id']
        # print('Model Fields:')
        # print(model_fields)
        
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            # print(reader)
            csv_header = reader.fieldnames # get all the header of the csv file
            
            
            # Compare CSV header with model's field names
            if csv_header != model_fields:
                raise DataError(f"CSV file does not match with the {model_name} table fields.")
            
            
            for row in reader:
                # print(row) : output = {'roll_no': '10050', 'name': 'James Turner', 'age': '19'}
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully!'))

# "C:\Users\ogwue\OneDrive\Desktop\Datasets\student_data.csv"