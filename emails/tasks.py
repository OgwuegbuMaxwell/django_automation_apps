import time
from apps_main.celery import app
from dataentry.utils import send_email_notifictation


@app.task
def send_email_task(mail_subject, message, to_email, attachement, email_id):
    send_email_notifictation(mail_subject, message, to_email, attachement, email_id)
    return 'Email sending task executed successfully.'

