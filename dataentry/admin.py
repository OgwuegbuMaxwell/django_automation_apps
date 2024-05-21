from django.contrib import admin

from dataentry.models import Customer, Student, Employee

class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'name', 'age')
    
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'country')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'designation', 'salary')


admin.site.register(Student, StudentAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Employee, EmployeeAdmin)