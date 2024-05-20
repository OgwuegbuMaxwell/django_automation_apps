# Add data to the database using custom command

from django.core.management.base import BaseCommand

from dataentry.models import Student



class Command(BaseCommand):
    help = "Insert data to the database"
    
    
    def handle(self, *args, **kwargs):
        # logic goes here
        
        # add 1 data
        # Student.objects.create(roll_no=1001, name='Ogwuegbu Maxwell', age=30)
        # self.stdout.write(self.style.SUCCESS('Data inserted succesfully!'))
        
        
        # insert multple data set
        dataset = [
            {'roll_no': 1002, 'name': 'Ekpechi Chizoba', 'age': 24},
            {'roll_no': 1003, 'name': 'Ogwuegbu Amarachi', 'age': 25},
            {'roll_no': 1004, 'name': 'Ekpo Victor', 'age': 31},
            {'roll_no': 1005, 'name': 'Iyeh Victor', 'age': 27},
            {'roll_no': 1006, 'name': 'Ogbenna Nnamdi', 'age': 32},
        ]
        
        for data in dataset:
            # print(data['name'])
            roll_no = data['roll_no']
            existing_record = Student.objects.filter(roll_no=roll_no).exists()
            
            if not existing_record:
                Student.objects.create(roll_no=data['roll_no'], name=data['name'], age=data['age'])
            else:
                self.stdout.write(self.style.WARNING(f'Student with roll no {roll_no} already exists!'))
           
        self.stdout.write(self.style.SUCCESS('Data inserted succesfully!'))




