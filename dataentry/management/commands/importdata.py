from django.core.management.base import BaseCommand, CommandError

from django.apps import apps

import csv

from django.db import DataError

from dataentry.utils import check_csv_errors



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
        
        model = check_csv_errors(file_path, model_name)
        
        with open(file_path, 'r') as file:
            reader = reader = csv.DictReader(file)
            for row in reader:
                # print(row) : output = {'roll_no': '10050', 'name': 'James Turner', 'age': '19'}
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully!'))

# "C:\Users\ogwue\OneDrive\Desktop\Datasets\student_data.csv"