from django.contrib import admin
from .models import Leave, Remaining_Leaves

# Register your models here.
admin.site.register(Leave)
admin.site.register(Remaining_Leaves)