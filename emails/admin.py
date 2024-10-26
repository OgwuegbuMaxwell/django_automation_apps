from django.contrib import admin
from .models import EmailTracking, List, Sent, Subscriber, Email
# Register your models here.


class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'email_list', 'sent_at')


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'email_list')


class EmailTrackingAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscriber', 'opened_at', 'clicked_at')

admin.site.register(List)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Email, EmailAdmin)

admin.site.register(EmailTracking, EmailTrackingAdmin)
admin.site.register(Sent)
