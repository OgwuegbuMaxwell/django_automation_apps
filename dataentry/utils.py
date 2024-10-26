import csv
import hashlib
import os
import time
from django.apps import apps
from django.core.management.base import CommandError
from django.db import DataError
import datetime


# email message
# email message takes 4 parameters
from django.core.mail import EmailMessage
from django.conf import settings


from apps_main.settings import BASE_URL
from emails.models import Email, EmailTracking, Sent, Subscriber

from bs4 import BeautifulSoup

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





def send_email_notifictation(mail_subject, message, to_email, attachment=None, email_id=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        for recipient_email in to_email:
            # Create Email tracking record
            new_message = message
            if email_id:
                email = Email.objects.get(pk=email_id)
                subscriber = Subscriber.objects.get(email_list=email.email_list, email_address=recipient_email)
                timestamp = str(time.time())
                data_to_hash = f"{recipient_email}{timestamp}"
                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
                email_tracking = EmailTracking.objects.create(
                    email = email,
                    subscriber = subscriber,
                    unique_id = unique_id
                )
                
                base_url = settings.BASE_URL
                # generate the tracking pixel
                click_tracking_url = f"{base_url}/emails/track/click/{unique_id}"
                # print('Tracking URL => ', click_tracking_url)
                
                # Generate Open tracking URL
                open_tracking_url = f"{base_url}/emails/track/open/{unique_id}"
                
                # search for the links in the email body
                soup = BeautifulSoup(message, 'html.parser')
                # for a in soup.find_all('a', href=True):
                #    print(a['href'])
                # Using list comprehension
                urls = [a['href'] for a in soup.find_all('a', href=True)] 
                
                # if there are links or urls in the email body, inject the click tracking url to the link
                if urls:
                    for url in urls:
                        # Final Tracking URL
                        tracking_url = f"{click_tracking_url}?url={url}"
                        # print('Final Tracking Url ====> ', tracking_url)
                        
                        # Replace the old urls in the messages with the tracking urls
                        new_message = new_message.replace(f"{url}", f"{tracking_url}")
                else:
                    print('No URLs found the email content')
                
                # Create the email content with tracking pixel image
                # we add open tracking image to the message whether the message
                # contains Urls or not
                open_tracking_img = f"<img src='{open_tracking_url}' width='1' height='1'>"
                new_message += open_tracking_img
                
                
            mail = EmailMessage(mail_subject, new_message, from_email, to=[recipient_email])
            if attachment is not None:
                mail.attach_file(attachment)
            
            mail.content_subtype = "html"
            mail.send()
        # Store the total sent emails inside the Sent Model
        if email_id:
            sent = Sent()
            sent.email = email
            sent.total_sent = email.email_list.count_emails()
            sent.save()
    except Exception as e:
        raise e





def generate_csv_file(model_name):
    
    # generate the timestamp of current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # define the csv file name/path
    
    export_dir = 'exported_data'
    
    file_name = f'imported_{model_name}_data_{timestamp}.csv'
    # print(file_name)
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    # print("File path = >", file_path)
    return file_path

