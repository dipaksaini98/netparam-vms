from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin

from .forms import EmployeeCreationForm, EmployeeChangeForm
from .models import Employee, Visit, Visitor, Event


class EmployeeAdmin(UserAdmin):
    add_form = EmployeeCreationForm
    form = EmployeeChangeForm
    model = Employee
    list_display = ['username', 'name', 'email']


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Visitor)
admin.site.register(Visit)
admin.site.register(Event)
