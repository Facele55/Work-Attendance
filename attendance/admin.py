from django.contrib import admin
from .models import CustomUser, WorkingHours, Holidays


admin.site.register(CustomUser)
admin.site.register(WorkingHours)
admin.site.register(Holidays)
