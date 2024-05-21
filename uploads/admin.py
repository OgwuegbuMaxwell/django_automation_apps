from django.contrib import admin

# Register your models here.

from .models import Upload

class UploadAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'file', 'uploaded_at')

admin.site.register(Upload, UploadAdmin)