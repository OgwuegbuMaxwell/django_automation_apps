from django.core.management.base import BaseCommand

# Proposed command = python manage.py greeting Maxwell
# Proposed output = Hi {name}, Good morning

class Command(BaseCommand):
    help = "Greet the user" # command level help test
    
    def add_arguments(self, parser):
        # the help test here is for the argument. argument help test
        parser.add_argument('name', type=str, help='specifies user name')
    
    def handle(self, *args, **kwargs):
        # Write the logic
        name = kwargs['name']
        greeting = f'Hi {name}, Good Morning'
        self.stdout.write(greeting)
        
        # in error format (in red text color)
        # self.stderr.write(greeting)
        
        # in success form
        # self.stdout.write(self.style.SUCCESS(greeting))
    