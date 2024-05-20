from django.contrib import admin

from dataentry.models import Customer, Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'name', 'age')
    
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'country')





admin.site.register(Student, StudentAdmin)

admin.site.register(Customer, CustomerAdmin)