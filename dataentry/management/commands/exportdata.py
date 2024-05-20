# '''
######### Exporting data from a single table ###########
# import csv
# from django.core.management.base import BaseCommand, CommandError

# from dataentry.models import Student
# import datetime

# # Proposed command: python manage.py exportdata


# class Command(BaseCommand):
#     help = "Export data from Student model to a CSV file"
    
#     def handle(self, *args, **kwargs):
#         # fetch the data from database
#         students = Student.objects.all()
#         # print(students)
        
#         # generate the timestamp of current date and time
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        
#         # define the csv file name/path
#         file_path = f'exported_students_data_{timestamp}.csv'
#         # print(file_path)
        
        
#         # open the csv file and write the data
#         with open(file_path, 'w', newline='') as file:
#             writer = csv.writer(file)
            
#             # Write the CSV header
#             writer.writerow(['Role No', 'Name', 'Age'])
            
#             # write data rows
#             for student in students:
#                 writer.writerow([student.roll_no, student.name, student.age])
        
#         self.stdout.write(self.style.SUCCESS('Data exported successfully!'))
    
        
# '''




########################################################################
######### Exporting data from any model you specifies ###########


import csv
from django.core.management.base import BaseCommand, CommandError, CommandParser

from django.apps import apps
import datetime

# Proposed command: python manage.py exportdata model_name


class Command(BaseCommand):
    
    help = "Export data from Student model to a CSV file"
    
    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Model name')

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name'].capitalize()
        
        # Search through all the installed apps for the model - makiking sure 
        # the model the user inputed exist
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break # stop executing once the model is found
            except LookupError:
                pass
        
        if not model:
            self.stderr.write(f'Model "{model}" cound not found')
            return
        
        # fetch the data from database
        data = model.objects.all()
        # print(data)
    
        # generate the timestamp of current date and time
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
        # define the csv file name/path
        file_path = f'imported_{model_name}_data_{timestamp}.csv'
        # print(file_path)
    
    
        # open the csv file and write the data
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
        
            # Write the CSV header
            # we want to print the field names of the model that we are trying to export
            writer.writerow([field.name for field in model._meta.fields])
        
            # write data rows
            for dt in data:
                writer.writerow([getattr(dt, field.name) for field in  model._meta.fields])
    
        self.stdout.write(self.style.SUCCESS('Data exported successfully!'))




