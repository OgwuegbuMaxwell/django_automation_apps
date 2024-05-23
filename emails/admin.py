from django.contrib import admin
from .models import List, Subscriber, Email
# Register your models here.


class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'email_list', 'sent_at')


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'email_list')

admin.site.register(List)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Email, EmailAdmin)
