from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


USER_TYPE_DATA = [
    ('1', _("ADMIN")),
    ('2', _("Staff")),
    ('3', _("Worker"))
]


WORK_PLACE_CHOICES = [
    ('remote', _("Praca Zdalna")),
    ('office', _("Biuro")),
    ('day_off', _("Weekend")),
    ('vacation', _("Urlop")),
    ('holiday', _("Święto")),
    ('seak_leave', _("Zwolnienie lekarskie")),
]


WORKING_STATUS_DATA = [
    ('currently', _('Currently Working')),
    ('fired', _('Fired'))
]


class CustomUser(AbstractUser):
    user_type = models.CharField(default='3', choices=USER_TYPE_DATA, max_length=10)
    status = models.CharField(choices=WORKING_STATUS_DATA, max_length=100, default='empty')
    work_position = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        ordering = ['-user_type']
        db_table = "user_table"


class WorkingHours(models.Model):
    """
    Model for storing working hours of worker
    wh = working hours
    """
    id = models.AutoField(primary_key=True)
    wh_date = models.DateField()
    wh_start = models.CharField(blank=True, max_length=100)
    wh_end = models.CharField(blank=True, max_length=100)
    wh_amount = models.CharField(max_length=100, blank=True)
    work_place = models.CharField(choices=WORK_PLACE_CHOICES, default='office', max_length=255)
    note = models.CharField(max_length=255, blank=True)
    worker = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    objects = models.Manager

    class Meta:
        verbose_name = "working hour"
        verbose_name_plural = "working hours"
        db_table = "working_hours"

    def __str__(self):
        return f"{self.worker}, {self.wh_date}"


class Holidays(models.Model):
    id = models.AutoField(primary_key=True)
    holi_date = models.DateField()
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Holiday (Day off)"
        verbose_name_plural = "Holidays (Days off)"
        db_table = "holidays"

    def __str__(self):
        return f"{self.holi_date} {self.name}"


class LoginLog(models.Model):
    id = models.AutoField(primary_key=True)
    worker = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    last_login = models.DateTimeField(null=True)
    last_logout = models.DateTimeField(null=True)

    class Meta:
        verbose_name = "working LoginLog"
        verbose_name_plural = "working LoginLogs"
        db_table = "login_log"

    def __str__(self):
        return f"{self.worker}"
