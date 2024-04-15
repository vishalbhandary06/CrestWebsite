from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

class EmployeeAdmin(UserAdmin):
    list_display = ('first_name', 'email', 'emp_id',)
    search_fields = ('email', 'first_name', 'emp_id',)
    readonly_fields = ('date_joined', 'last_login',)

    filter_horizontal = ()
    list_filter = ('first_name',)
    fieldsets = ()
    ordering = ('first_name',)

    add_fieldsets = (
        (
            None,{
                'classes' : ('wide',),
                'fields' : ('email', 'first_name', 'emp_id', 'password1', 'password2', 'position','is_staff', 'is_admin',)
            }
        ),
    )
    

# Register your models here.
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Title)
admin.site.register(Position)
admin.site.register(Emergency)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Relationship)
admin.site.register(Education)