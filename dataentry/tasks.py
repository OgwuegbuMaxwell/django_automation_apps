import time
from apps_main.celery import app
from django.core.management import call_command


# email message
# email message takes 4 parameters
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import generate_csv_file, send_email_notifictation


@app.task
def celery_test_task():
    time.sleep(5) # Simulation of any time that's going to take 10 seconds
    mail_subject = 'Test subject'
    message = 'Test message v2'
    to_email = settings.DEFAULT_TO_EMAIL
    # send_email_notifictation(mail_subject, message, to_email)
    return 'Task Executed successfully'



@app.task
def import_data_task(file_path, model_name):
    # Triger the importdata command
    try:
        call_command('importdata', file_path, model_name)
    except Exception as e:
        raise e
    # notify the user
    mail_subject = 'Import Data Completed'
    message = 'Your data has been imported successfully'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notifictation(mail_subject, message, [to_email])
    return 'Data Imported Successfully!'
        


@app.task
def export_data_task(model_name):
    # Triger the exportdata command
    try:
        call_command('exportdata',model_name)
    except Exception as e:
        raise e
    
    file_path = generate_csv_file(model_name)
    # print("file path => ", file_path)
    
    # send email with the attachment
    # notify the user
    mail_subject = 'Export Data Successful'
    message = 'Export data successfully, please find the attachment'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notifictation(mail_subject, message, [to_email], attachment=file_path)
    return 'Export data executed successfully.'
    


