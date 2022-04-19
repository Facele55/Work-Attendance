# Generated by Django 3.2.7 on 2021-11-08 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_customuser_work_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='Holidays',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('holi_date', models.DateField()),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Holiday (Day off)',
                'verbose_name_plural': 'Holidays (Days off)',
                'db_table': 'holidays',
            },
        ),
        migrations.AlterField(
            model_name='workinghours',
            name='work_place',
            field=models.CharField(choices=[('remote', 'Praca Zdalna'), ('office', 'Biuro'), ('day_off', 'Weekend'), ('vacation', 'Urlop'), ('holiday', 'Święto')], default='office', max_length=255),
        ),
    ]
