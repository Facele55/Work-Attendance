import datetime
import logging
from typing import Any

import babel.dates
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.shortcuts import redirect
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView, UpdateView, DeleteView
from xhtml2pdf import pisa

from .forms import RegisterEntry, LoginForm, EditRecord
from .forms import SendMailForm
from .models import WorkingHours, CustomUser, Holidays
from .services.helpers import wh_norma, calculate_wh_amount, log_in_out
from .services.int_or_float import is_int_or_float

logger = logging.getLogger('django')


def login_view(request):
    """
    Login view and login user
    """
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                log_in_out(user_id=user.id, status=2)
                logger.info("User %s logged in successfully, headers %s", str(user), str(request.headers))
                return redirect("/")
            else:
                messages.error(request, _("Podano nieprawidłowe dane"))
                logger.warning("Wrong credentials, %s", str(request.headers))
        else:
            messages.error(request, _('Błąd walidacji formularza'))
            logger.error("Login_view, Form validation Error")
    return render(request, "attendance/login.html", {"form": form})


def logout_out(request):
    log_in_out(user_id=request.user.id, status=1)
    logger.info("User %s logged out successfully, headers %s", str(request.user), str(request.headers))
    logout(request)
    return HttpResponseRedirect('/')


class RegisterEntryView(FormView):
    """
    View to register worker's entry to work, place and time (from and until)
    """
    template_name = 'attendance/submit_entry.html'
    form_class = RegisterEntry
    success_url = reverse_lazy('attendance:entry')

    def form_valid(self, form):
        wh_start = form.cleaned_data.get("wh_start")
        wh_end = form.cleaned_data.get("wh_end")
        wh_date = form.cleaned_data.get("wh_date")
        place = form.cleaned_data.get("work_place")
        note = form.cleaned_data.get("note")
        user_id = self.request.user.id
        register_entry_save(user_id=user_id, wh_start=wh_start, wh_end=wh_end, wh_date=wh_date, place=place, note=note)
        logger.info("User %d submitted work entry; \n date: %s,  place: %s, start time: %s, end time: %s, note: %s",
                    user_id, wh_date, place, wh_start, wh_end, note)
        messages.success(self.request, _('Witamy w prace!'))
        return HttpResponseRedirect(self.get_success_url())


def register_entry_save(user_id: int, wh_start: str, wh_end: str, wh_date: datetime.date, place: str, note: str):
    """
    Custom f-n for saving to db Wh with some additional calculations like amount of wh,
    empty time string,
    """
    if place == 'day_off' or place == 'vacation' or place == 'holiday' or place == 'seak_leave':
        try:
            WorkingHours.objects.create(worker_id=user_id, wh_start="", wh_end="", wh_date=wh_date, work_place=place,
                                        note=note).save()
        except ValueError as ve:
            logger.error("Register_entry_save, if statement, Value error: %s", str(ve))
        except Exception as e:
            logger.exception("Register_entry_save, if statement, exception: %s", str(e))
    else:
        try:
            WorkingHours.objects.create(worker_id=user_id, wh_start=wh_start, wh_end=wh_end, wh_date=wh_date,
                                        wh_amount=calculate_wh_amount(wh_start, wh_end), work_place=place,
                                        note=note).save()
        except ValueError as ve:
            logger.error("Register_entry_save, else statement, Value error: %s", str(ve))
        except Exception as e:
            logger.exception("Register_entry_save, else statement, exception: %s", str(e))


def tables(request):
    """
    Table to show all worked hours, regrouped by year and month on template
    """
    dt = datetime.datetime.today()
    context = {
        "hours": WorkingHours.objects.all().order_by('-wh_date'),
        "total": count_total_wh_hours(user_id=request.user.id, month_id=dt.month, year_id=dt.year),
        "holidays": Holidays.objects.all(),
    }
    return render(request, 'attendance/attend_table.html', context)


def count_total_wh_hours(user_id: int, month_id: int, year_id: int) -> Any:
    """
    Aggregate wh from table and return amount
    """
    try:
        total = WorkingHours.objects.all().filter(worker_id=user_id).filter(wh_date__month=month_id).filter(
            wh_date__year=year_id).aggregate(wh_sum=Sum('wh_amount'))['wh_sum']
        return is_int_or_float(number=total)
    except Exception as e:
        logger.exception("Count_total_wh_hours, exception: %s", str(e))
        total = 0
    return total 


def delete_record(request, record_id: int):
    """
    Deleting WH record
    """
    try:
        wh = WorkingHours.objects.get(id=record_id)
        wh.delete()
        messages.success(request, _("Usunieto"))
    except WorkingHours.DoesNotExist:
        logger.exception("Delete_record, record WorkingHours.DoesNotExist: %d", record_id)
        messages.error(request, "Nie Istnieje")
        return redirect('attendance:tables')
    except Exception as e:
        logger.exception("Delete_record: exception %s", str(e))
        messages.error(request, "Błąd " + str(e))
    return redirect('attendance:tables')


def month_report_view(request, user_id: int, month_id: int, year_id: int) -> HttpResponse:
    """
    This f-n generate month report with for user = user_id, for given month and year
    and
    """
    holy_days = Holidays.objects.all().filter(holi_date__year=year_id, holi_date__month=month_id)
    try:
        hours = WorkingHours.objects.all().order_by('wh_date').filter(worker_id=user_id).filter(
            wh_date__month=month_id).filter(wh_date__year=year_id)
    except CustomUser.DoesNotExist:
        logger.exception("Month_report_view, record CustomUser.DoesNotExist: %d", user_id)
        return redirect('attendance:workers_table')
    except Exception as ex:
        logger.exception("Month_report_view, exception: %s", str(ex))
        return redirect('attendance:workers_table')
    template = get_template("attendance/reports.html")
    html = template.render({"hours": hours, "worker": CustomUser.objects.get(id=user_id),
                            "total": count_total_wh_hours(user_id=user_id, month_id=month_id, year_id=year_id),
                            "month": babel.dates.get_month_names('wide', context='stand-alone',
                                                                 locale=request.LANGUAGE_CODE)[month_id],
                            "year": year_id,
                            "norma": wh_norma(month_id, year_id),
                            "holidays": holy_days})
    file = open('report.pdf', "w+b")
    pisa.CreatePDF(html.encode('UTF-8'), dest=file)
    file.seek(0)
    pdf = file.read()
    file.close()
    return HttpResponse(pdf, 'application/pdf')


class EditRecordView(UpdateView):
    model = WorkingHours
    template_name = 'attendance/edit_record.html'
    success_url = reverse_lazy('attendance:tables')
    pk_url_kwarg = 'record_id'
    form_class = EditRecord

    def form_valid(self, form):
        wh_start = form.cleaned_data.get("wh_start")
        wh_end = form.cleaned_data.get("wh_end")
        wh = form.save(commit=False)
        wh.wh_amount = calculate_wh_amount(wh_start, wh_end)
        wh.save()
        form.save_m2m()
        #  print(self.kwargs.get("record_id"), self.request.user)
        logger.info("User %s changed record_id %d on date: %s", self.request.user, self.kwargs.get("record_id"),
                    str(datetime.datetime.now()))
        messages.success(self.request, _('Aktualizowano!'))
        return HttpResponseRedirect(self.get_success_url())


class DeleteRecord(DeleteView):
    model = WorkingHours
    success_url = reverse_lazy('attendance:tables')
    pk_url_kwarg = 'record_id'


def simple_send_mail(request):
    if request.method == 'POST':
        form = SendMailForm(request.POST or None)
        if form.is_valid():
            to_mail = form.cleaned_data['email_to']
            members = form.cleaned_data['members']
            period = form.cleaned_data['period']
            #  print(members, period.month, period.year)
            mon = babel.dates.get_month_names('wide', context='stand-alone', locale=request.LANGUAGE_CODE)[period.month]
            subject = _("Monthly reports")
            message = "Monthly reports for month: {}, year: {}".format(mon, period.year)
            for i in members:
                us = CustomUser.objects.get(username=i)

                attach = month_report_view(user_id=us.id, month_id=period.month, year_id=period.year, request=request)
                try:
                    mail = EmailMessage(subject=subject, body=message, to=[to_mail])
                    for file in attach:
                        mail.attach("{}-{}_{}_{}.pdf".format(us.first_name, us.last_name, period.month, period.year),
                                    file)
                    mail.send()
                except ArithmeticError as aex:
                    print(aex.args)
                    return HttpResponse('Invalid header found')
            messages.success(request, "Mails Sent Successfully")
            return redirect('attendance:send_email')
    else:
        form = SendMailForm()
    return render(request, 'attendance/send_mail.html', {'form': form})
