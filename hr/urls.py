from django.urls import path

from .views import *

app_name = 'hr'


urlpatterns = [path('edit_usr/<int:usr_id>', EditUsers.as_view(), name="edit_user"),
    path('edit_user_perm/<int:usr_id>', EditPermUsers.as_view(), name="edit_user_perm"),
    path('hr', see_users, name="hr"), path('add_user/', AddUser.as_view(), name="add_user"),
    path('delete_user/<int:user_id>', DeleteUser.as_view(), name="delete_user"),

    path('edit_holiday/<int:holy_id>', EditHolidayView.as_view(), name="edit_holiday"),
    path('delete_holiday/<int:holy_id>', delete_holiday, name="delete_holiday"),
    path('login_table/', login_table, name="login_table"), path('holiday_table/', holiday_table, name="holiday_table"),
    path('add_holiday/', AddHoliday.as_view(), name="add_holiday"),

]
