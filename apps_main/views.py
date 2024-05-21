from django.http import HttpResponse
from django.shortcuts import render
from dataentry.tasks import celery_test_task

def home(request):
    return render(request, 'home.html')


def celery_test(request):
    # Execut time consumming task
    celery_test_task.delay()
    return HttpResponse('Function Executed Successfully')