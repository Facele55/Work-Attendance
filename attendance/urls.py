from django.urls import path

from .views import *

app_name = 'attendance'

urlpatterns = [path('', RegisterEntryView.as_view(), name="index"),
    path('entry/', RegisterEntryView.as_view(), name="entry"), path('table/', tables, name="tables"),
    path('login/', login_view, name="login"), path('logout/', logout_out, name="logout"),
    path('delete_record/<int:record_id>', delete_record, name="delete_record"),
    path('edit_record/<int:record_id>', EditRecordView.as_view(), name="edit_record"),

    path('month_report_view/<int:user_id>/<int:month_id>/<int:year_id>', month_report_view, name="month_report"),

    path('send_email', simple_send_mail, name="send_email")]
