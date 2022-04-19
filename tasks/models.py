from django.db import models
from django.utils.translation import ugettext_lazy as _


STATUSES = [
        ('to-do', _('To Do')),
        ('in_progress', _('In Progress')),
        ('blocked', _('Blocked')),
        ('done', _('Done')),
        ('dismissed', _('Dismissed'))
]
PRIORITIES = [
        ('low', _('Low')),
        ('normal', _('Normal')),
        ('high', _('High')),
        ('critical', _('Critical')),
        ('blocker', _('Blocker'))
]


class Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField(null=True,blank=True)
    end_date = models.DateTimeField(null=True,blank=True)
    state = models.CharField(_("state"), max_length=20, choices=STATUSES, default='to-do')
    priority = models.CharField(_("priority"), max_length=20, choices=PRIORITIES, default='normal')

    def __str__(self):
        return f"self.name"

