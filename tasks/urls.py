from django.urls import path

from .views import *

app_name = 'tasks'

urlpatterns = [
    path('all_tasks/', all_tasks, name="all_tasks"),

]
