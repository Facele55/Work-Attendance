from django.urls import path

from attendance.LoginCheckMiddleWare import role_redirect
from .views import *

app_name = 'users'


urlpatterns = [
    # General URLs
    path('', role_redirect, name="index"),
    path('profile/', user_profile, name="profile"),
    path('profile_update/', profile_update, name="profile_update"),
    path('change-password/', UpdatePassword.as_view(), name="update_password"),
    # Admin
    path('admin_home/', admin_home, name="admin_home"),
    # HR
    path('hr_home/', hr_home, name="hr_home"),
    # Worker
    path('worker_home/', worker_home, name="worker_home"),
]
