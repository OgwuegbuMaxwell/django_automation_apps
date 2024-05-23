from django.conf import settings
from django.shortcuts import redirect, render
from emails.forms import EmailForm
from django.contrib import messages

from dataentry.utils import send_email_notifictation
from emails.models import Subscriber
from emails.tasks import send_email_task

# Create your views here.

def send_email(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email_form = email_form.save()
            
            # Send an email
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            email_list = request.POST.get('email_list')
            # print("Email List => ", email_list) Email List =>  3  (the id)
            
            # Access the selected email list
            email_list = email_form.email_list
            # print("Email List => ", email_list) #Email List =>  Developers (subscriber name)
            
            # Extract Email addresses from subscribers model in the selected email list
            subscribers = Subscriber.objects.filter(email_list=email_list)
            
            
            # store all the subscribers to to_email
            # to_email = []
            # for email in subscribers:
            #     to_email.append(email.email_address)
            # print("Email List => ", to_email) 
            # the above commented is the same below using list comprehension
            to_email = [email.email_address for email in subscribers]
            
            # Check if there's attachment
            if email_form.attachment:
                attachement = email_form.attachment.path
            else:
                attachement = None
            
            # send the email using celery || or send it here directly
            # send_email_notifictation(mail_subject, message, to_email, attachement)
            # using celery below. hand over email sending task to celery
            send_email_task.delay(mail_subject, message, to_email, attachement)
            
            
            # display a success message
            messages.success(request, 'Email sent successfully!')
            return redirect('send_email')
    else:
        email_form = EmailForm()
        context = {
            'email_form':email_form
        }
        return render(request, 'emails/send-email.html', context)


