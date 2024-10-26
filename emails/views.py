from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from emails.forms import EmailForm
from django.contrib import messages

from dataentry.utils import send_email_notifictation
from emails.models import Email, Sent, Subscriber, EmailTracking
from emails.tasks import send_email_task
from django.db.models import Sum
from django.utils import timezone

# Create your views here.

def send_email(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email = email_form.save()
            
            # Send an email
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            email_list = request.POST.get('email_list')
            # print("Email List => ", email_list) Email List =>  3  (the id)
            
            # Access the selected email list
            email_list = email.email_list
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
            if email.attachment:
                attachement = email.attachment.path
            else:
                attachement = None
            
            
            email_id = email.id
                
            
            # send the email using celery || or send it here directly
            # send_email_notifictation(mail_subject, message, to_email, attachement)
            # using celery below. hand over email sending task to celery
            send_email_task.delay(mail_subject, message, to_email, attachement, email_id)
            
            
            # display a success message
            messages.success(request, 'Email sent successfully!')
            return redirect('send_email')
    else:
        email = EmailForm()
        context = {
            'email_form':email
        }
        return render(request, 'emails/send-email.html', context)




def track_click(request, unique_id):
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        url = request.GET.get('url')
        # Check if the clicked_at field is set or not
        if not email_tracking.clicked_at:
            email_tracking.clicked_at = timezone.now()
            email_tracking.save()
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect(url)
    except:
        return HttpResponse("Email Tracking Record Not Found")
        
        
    



def track_open(request, unique_id):
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        # Check if the open_at field is set or not
        if not email_tracking.opened_at:
            email_tracking.opened_at = timezone.now()
            email_tracking.save()
            return HttpResponse("Email opened successfully")
        else:
            print('Email already opened')
            return HttpResponse("Email already opened")
    except: 
        return HttpResponse("Email Tracking Record Not Found")
        
    


def track_dashboard(request):
    # annotate(total_sent=Sum('sent__total_sent') 
    # this create new field in the email model called total_sent.
    # the total sent will be assigned to each of the eamil object
    emails = Email.objects.all().annotate(total_sent=Sum('sent__total_sent')).order_by('-sent_at')
    
    
    context = {
        'emails': emails
    }
    return render(request, 'emails/track_dashboard.html', context)


def track_stats(request, pk):
    email = get_object_or_404(Email, pk=pk)
    sent = Sent.objects.get(email=email)
    context = {
        'email': email,
        'total_sent': sent.total_sent
    }
    return render(request, 'emails/track_stats.html', context)