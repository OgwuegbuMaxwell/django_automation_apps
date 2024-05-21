from django.conf import settings
from django.shortcuts import redirect, render

from dataentry.utils import check_csv_errors, get_all_custom_models
from uploads.models import Upload
# from django.core.management import call_command
from django.contrib import messages
from dataentry.tasks import import_data_task

# Create your views here.



def import_data(request):
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')
        # print('file path =>', file_path)
        # print('Model Name =>', model_name)
        # return redirect('import_data')
        
        # Store this file inside the Upload model
        uplaod = Upload.objects.create(file=file_path, model_name=model_name)
        
        
        # Construct the full path
        relative_path = str(uplaod.file.url)
        # print(relative_path)
        base_url = str(settings.BASE_DIR)
        # print(base_url + relative_path)
        file_path = base_url + relative_path
        # print(file_path)
        
        # Check for errors
        try:
            check_csv_errors(file_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import_data')
        
        # Handle the import data task here
        import_data_task.delay(file_path, model_name)
        
        # Show message to the user (you data is being imported and will notify you when it's done)
        messages.success(request, "You data is being imported, you will be notify when it's done")
        
        return redirect('import_data')
        
    else:
        custom_models = get_all_custom_models()
        # print(all_models)
        
        context = {
            'custom_models': custom_models
        }
    return render(request, 'dataentry/importdata.html', context)
