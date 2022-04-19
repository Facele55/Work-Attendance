from django.forms import ModelForm, widgets
from django.utils.translation import gettext_lazy as _

from attendance.models import CustomUser


class AddUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
        exclude = ['password', 'user_permissions', 'groups', 'is_active', 'is_superuser', 'is_staff', 'username']
        labels = {'username': _("Username"),
                  "first_name": _("First Name"),
                  "last_name": _("Last Name"),
                  "email": _("Email address"),
                  "user_type": _("User Type"),
                  "status": _("Status"),
                  "work_position": _("Work Position"),
                  }

        widgets = {
            'username': widgets.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "first_name": widgets.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "last_name": widgets.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "email": widgets.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "user_type": widgets.Select(
                attrs={
                    'class': "form-select bg-white"
                }
            ),
            "status": widgets.Select(
                attrs={
                    'class': "form-select bg-white"}),
            "work_position": widgets.TextInput(attrs={"class": "form-control"}), }


class UpdateUser(ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
        exclude = ['password', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']
        labels = AddUserForm.Meta.labels
        widgets = AddUserForm.Meta.widgets


class EditUserPermForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
        labels = AddUserForm.Meta.labels
        widgets = AddUserForm.Meta.widgets
        exclude = ['password', ]
