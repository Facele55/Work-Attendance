# Generated by Django 3.2.7 on 2021-11-02 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='work_position',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
