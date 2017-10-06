# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-04 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festivalapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Festival',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='OldFestival',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('festivals', models.ManyToManyField(to='festivalapp.Festival')),
            ],
        ),
        migrations.AddField(
            model_name='band',
            name='is_booked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='concert',
            name='genre',
            field=models.CharField(choices=[('rock', 'ROCK'), ('pop', 'POP'), ('electric', 'ELECTRIC')], default=None, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employee_status',
            field=models.CharField(choices=[('arranger', 'ARRANGER'), ('sound_technician', 'LYDTEKNIKER'), ('light_technician', 'LYSTEKNIKER'), ('manager', 'MANAGER'), ('booking_responsible', 'BOOKINGANSVARLIG')], max_length=32),
        ),
        migrations.AddField(
            model_name='festival',
            name='concerts',
            field=models.ManyToManyField(to='festivalapp.Concert'),
        ),
    ]