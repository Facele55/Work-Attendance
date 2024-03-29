# Generated by Django 3.2.7 on 2022-02-03 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='task_type',
        ),
        migrations.AddField(
            model_name='tasks',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('normal', 'Normal'), ('high', 'High'), ('critical', 'Critical'), ('blocker', 'Blocker')], default='normal', max_length=20, verbose_name='priority'),
        ),
        migrations.AddField(
            model_name='tasks',
            name='state',
            field=models.CharField(choices=[('to-do', 'To Do'), ('in_progress', 'In Progress'), ('blocked', 'Blocked'), ('done', 'Done'), ('dismissed', 'Dismissed')], default='to-do', max_length=20, verbose_name='state'),
        ),
    ]
