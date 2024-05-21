import csv
from django.apps import apps
from django.core.management.base import CommandError
from django.db import DataError

# email message
# email message takes 4 parameters
from django.core.mail import EmailMessage
from django.conf import settings

def get_all_custom_models():
    default_models = ['LogEntry', 'Permission', 'Group', 'ContentType', 'Session', 'User', 'Upload']
    # try to get all the apps
    custom_models = []
    
    for model in apps.get_models():
        # print(model)
        # print(model.__name__)
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
    return custom_models
        


def check_csv_errors(file_path, model_name):
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
    
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            # print(reader)
            csv_header = reader.fieldnames # get all the header of the csv file
            
            
            # Compare CSV header with model's field names
            if csv_header != model_fields:
                raise DataError(f"CSV file does not match with the {model_name} table fields.")
    except Exception as e:
        raise e        
    
    return model   





def send_email_notifictation(mail_subject, message, to_email):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
        mail.send()
    except Exception as e:
        raise e


