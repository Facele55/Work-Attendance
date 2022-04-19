import datetime
import logging

import numpy as np
from django.utils import timezone

from attendance.models import Holidays, CustomUser, LoginLog
from attendance.services.int_or_float import is_int_or_float

logger = logging.getLogger('django')


def wh_norma(month_id: int, year_id: int) -> int:
    """
    Calculate planned amount of working hours in given month.
    Planned amount of WH per day is 8 H, so this f-n just multiply business days by 8
    """
    norma = calc_holidays(month_id, year_id)
    return norma * 8


def calc_holidays(month_id: int, year_id: int) -> int:
    """
    Calculate business days or working days in particular month, year.
    Also obtain holidays
    """
    start_date = datetime.date(year_id, month_id, 1)
    if month_id == 12:
        end_date = datetime.date(year_id + 1, 1, 1)
    else:
        end_date = datetime.date(year_id, month_id + 1, 1)
    holi_day = Holidays.objects.all().filter(holi_date__year=year_id, holi_date__month=month_id)
    h = []
    days = 0
    if holi_day:
        for i in holi_day:
            h.append(i.holi_date)
            days = np.busday_count(start_date, end_date, weekmask=[1, 1, 1, 1, 1, 0, 0], holidays=h)
        return days
    else:
        days = np.busday_count(start_date, end_date)
        return days


def calculate_wh_amount(wh_start: str, wh_end: str):
    time_format = "%H:%M"
    time_delta = datetime.datetime.strptime(wh_end, time_format) - datetime.datetime.strptime(wh_start, time_format)
    hours_min = time_delta.total_seconds() / 3600
    return is_int_or_float(number=hours_min)


def log_in_out(user_id: int, status: int):
    """
    For adding to db record who and when was logged in or logged out.
    This made for full control
    """
    user = CustomUser.objects.get(id=user_id)
    if status == 1:
        try:
            LoginLog.objects.create(worker=user, last_logout=timezone.now())
        except Exception as ex:
            logger.exception("Function log_in_out, for status 1 (logout) got exception %s ", str(ex))
    else:
        try:
            LoginLog.objects.create(worker=user, last_login=timezone.now())
        except Exception as e:
            logger.exception("Function log_in_out, for status 2 (login) got exception %s ", str(e))
