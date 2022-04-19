import datetime
import logging
import random

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import UpdateView, FormView, DeleteView

from attendance.forms import AddHolidayForm
from attendance.models import CustomUser, Holidays, LoginLog
from hr.forms import AddUserForm, EditUserPermForm

logger = logging.getLogger('django')


def see_users(request):
    return render(request, 'hr/hr.html', {"users": CustomUser.objects.all()})


class EditUsers(UpdateView):
    model = CustomUser
    template_name = 'hr/edit_user.html'
    success_url = reverse_lazy('hr:hr')
    pk_url_kwarg = 'usr_id'
    form_class = EditUserPermForm

    def form_valid(self, form):
        form.save()
        logger.info("User %s changed user_id %d on date: %s", self.request.user, self.kwargs.get("usr_id"),
                    str(datetime.datetime.now()))
        messages.success(self.request, _('Aktualizowano!'))
        return HttpResponseRedirect(self.get_success_url())


class EditPermUsers(UpdateView):
    model = CustomUser
    template_name = 'hr/edit_user_perm.html'
    success_url = reverse_lazy('hr:hr')
    pk_url_kwarg = 'usr_id'
    form_class = EditUserPermForm

    def form_valid(self, form):
        form.save()
        logger.info("User %s changed user_id %d on date: %s", self.request.user, self.kwargs.get("usr_id"),
                    str(datetime.datetime.now()))
        messages.success(self.request, _('Aktualizowano!'))
        return HttpResponseRedirect(self.get_success_url())


class AddHoliday(FormView):
    """
    For adding holiday to db, table Holidays
    """
    template_name = 'hr/holidays.html'
    form_class = AddHolidayForm
    success_url = reverse_lazy('hr:add_holiday')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('Dodano!'))
        return HttpResponseRedirect(self.get_success_url())


class EditHolidayView(UpdateView):
    model = Holidays
    template_name = 'hr/edit_holiday.html'
    success_url = reverse_lazy('hr:holiday_table')
    pk_url_kwarg = 'holy_id'
    form_class = AddHolidayForm

    def form_valid(self, form):
        form.save()
        #  print(self.kwargs.get("holy_id"), self.request.user)
        logger.info("User %s changed Holiday holy_id %d on date: %s",
                    self.request.user, self.kwargs.get("holy_id"), str(datetime.datetime.now()))
        messages.success(self.request, _('Aktualizowano!'))
        return HttpResponseRedirect(self.get_success_url())


def holiday_table(request):
    """
    Show all holidays from table
    """
    return render(request, 'hr/holidays.html', {"holiday": Holidays.objects.all().order_by('holi_date')})


def login_table(request):
    """
    Show all login logs from table
    """
    return render(request, 'hr/login_table.html', {"login_log": LoginLog.objects.all().order_by('-id')})


def delete_holiday(request, holy_id: int):
    """
    Delete Holiday
    """
    try:
        h = Holidays.objects.get(id=holy_id)
        h.delete()
        messages.success(request, _("Usunieto"))
    except Holidays.DoesNotExist:
        logger.exception("Delete Holiday, Holidays.DoesNotExist: %d", holy_id)
        messages.error(request, _("Nie Istnieje"))
        return redirect('hr:holiday_table')
    except Exception as e:
        logger.exception("Delete Holiday, exception: %s", str(e))
        messages.error(request, _("Błąd") + str(e))
    return redirect('hr:holiday_table')


class AddUser(FormView):
    template_name = 'hr/create_user.html'
    success_url = reverse_lazy('hr:hr')
    form_class = AddUserForm

    def form_valid(self, form):
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        username = generate_username(first_name, last_name)
        password = generate_password(first_name, last_name)
        print(username, password)
        c_user = form.save(commit=False)
        c_user.username = generate_username(first_name, last_name)
        c_user.set_password(password)
        #c_user.password = generate_password(first_name, last_name)
        c_user.save()
        form.save_m2m()
        messages.success(self.request, _('Profile was created successfully!'))
        return HttpResponseRedirect(self.get_success_url())


class DeleteUser(DeleteView):
    model = CustomUser
    success_url = reverse_lazy('hr:hr')
    pk_url_kwarg = 'user_id'


def generate_username(first_name: str, last_name: str) -> str:
    number = '{:03d}'.format(random.randrange(1, 999))
    username = (first_name.lower() + last_name.lower() + number)
    return _check_username_existence(username=username)


def generate_password(first_name: str, last_name: str) -> str:
    gen_password = first_name.lower()
    return gen_password


def _check_username_existence(username: str) -> str:
    if not CustomUser.objects.all().filter(username=username).exists():
        return username
    else:
        number_2 = '{:02d}'.format(random.randrange(1, 99))
        new_username = username + number_2
        return new_username
