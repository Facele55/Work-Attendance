# Generated by Django 3.2.7 on 2021-11-11 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_loginlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginlog',
            name='last_login',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='loginlog',
            name='last_logout',
            field=models.DateTimeField(null=True),
        ),
    ]
