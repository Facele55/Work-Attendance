import datetime

from django import forms
from django.forms import ModelForm, widgets
from django.utils.translation import gettext_lazy as _

from .models import WorkingHours, Holidays, CustomUser

dt = datetime.datetime.now()


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Username"),
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Password"),
                "class": "form-control", 'autocomplete': 'off', 'data-toggle': 'password'
            }
        ))


class RegisterEntry(ModelForm):
    class Meta:
        exclude = ['worker', 'wh_amount']
        model = WorkingHours
        fields = '__all__'
        labels = {
            'wh_start': _("Godzina pracy od"),
            "wh_end": _("Godzina pracy do"),
            "wh_date": _("Data"),
            "work_place": _("Miejsce pracy"),
            "note": _("Notatka")
        }
        widgets = {
            'wh_date': widgets.TextInput(
                attrs={
                    "type": "date",
                    'class': 'form-control bg-white',
                    "value": dt.today().date(),
                   }
            ),
            'wh_start': widgets.TimeInput(
                attrs={'type': 'time-local',
                       'class': 'timepicker form-control bg-white',
                       'required': False,
                       }
            ),
            'wh_end': widgets.TimeInput(
                attrs={
                    'type': 'time-local',
                    'class': 'timepicker form-control bg-white',
                    'required': False
                }
            ),
            'work_place': widgets.Select(
                attrs={
                    'class': "form-select bg-white"
                }
            ),
            'note': widgets.Textarea(
                attrs={
                    'class': 'form-control bg-white',
                    'rows': '2',
                    'cols': '2',
                }
            )
        }


class AddHolidayForm(ModelForm):
    class Meta:
        model = Holidays
        fields = '__all__'
        labels = {
            "name": _("Nazwa Święta"),
            "holi_date": _("Data Święta")
        }
        widgets = {
            "name": widgets.TimeInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "holi_date": widgets.TextInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            )
        }


class EditRecord(RegisterEntry):
    class Meta:
        model = WorkingHours
        exclude = RegisterEntry.Meta.exclude + ['wh_date', 'work_place']
        fields = RegisterEntry.Meta.fields
        labels = RegisterEntry.Meta.labels
        widgets = RegisterEntry.Meta.widgets


class SendMailForm(forms.Form):
    email_to = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control bg-white'}))
    members = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': ''}))
    period = forms.DateField(widget=forms.TextInput(attrs={"type": "date", 'class': 'form-control bg-white'}))
