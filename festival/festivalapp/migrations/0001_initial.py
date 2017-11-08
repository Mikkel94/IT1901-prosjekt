# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-08 13:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, null=True)),
                ('members', models.IntegerField(default=1, null=True)),
                ('light_needs', models.IntegerField(default=0)),
                ('sound_needs', models.IntegerField(default=0)),
                ('specific_needs', models.TextField(default='No specific needs yet')),
                ('is_booking_req_sendt', models.BooleanField(default=False)),
                ('is_booked', models.BooleanField(default=False)),
                ('sold_albums', models.IntegerField(default=100)),
                ('former_concerts', models.IntegerField(default=1)),
                ('review', models.TextField(default='No review yet')),
                ('contact_info', models.EmailField(blank=True, max_length=254)),
                ('links', models.CharField(blank=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Concert', max_length=50)),
                ('genre', models.CharField(choices=[('Rock', 'ROCK'), ('Pop', 'POP'), ('Electric', 'ELECTRIC')], default=None, max_length=32, null=True)),
                ('start_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('audience', models.IntegerField(default=0)),
                ('date', models.DateField()),
                ('price', models.IntegerField(default=100)),
                ('ticket_sales', models.IntegerField(default=0)),
                ('band', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='band', to='festivalapp.Band')),
            ],
        ),
        migrations.CreateModel(
            name='ConcertRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Concert', max_length=50)),
                ('genre', models.CharField(choices=[('Rock', 'ROCK'), ('Pop', 'POP'), ('Electric', 'ELECTRIC')], default=None, max_length=32, null=True)),
                ('price', models.IntegerField(default=100)),
                ('date', models.DateField()),
                ('start_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('is_sendt', models.BooleanField(default=False)),
                ('band', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='festivalapp.Band')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_status', models.CharField(choices=[('ARRANGER', 'ARRANGER'), ('LYDTEKNIKER', 'LYDTEKNIKER'), ('LYSTEKNIKER', 'LYSTEKNIKER'), ('MANAGER', 'MANAGER'), ('BOOKINGANSVARLIG', 'BOOKINGANSVARLIG'), ('BOOKINGSJEF', 'BOOKINGSJEF'), ('PR-MANAGER', 'PR-MANAGER'), ('SERVICE MANAGER', 'SERVICE MANAGER'), ('BAND MEMBER', 'BAND MEMBER')], max_length=32)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Festival',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Scene', max_length=50)),
                ('capacity', models.IntegerField(default=300)),
            ],
        ),
        migrations.AddField(
            model_name='concertrequest',
            name='festival',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='festivalapp.Festival'),
        ),
        migrations.AddField(
            model_name='concertrequest',
            name='scene',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='festivalapp.Scene'),
        ),
        migrations.AddField(
            model_name='concert',
            name='festival',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='festival', to='festivalapp.Festival'),
        ),
        migrations.AddField(
            model_name='concert',
            name='lighting_work',
            field=models.ManyToManyField(blank=True, related_name='lighting', to='festivalapp.Employee'),
        ),
        migrations.AddField(
            model_name='concert',
            name='scene',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='festivalapp.Scene'),
        ),
        migrations.AddField(
            model_name='concert',
            name='sound_work',
            field=models.ManyToManyField(blank=True, related_name='sound', to='festivalapp.Employee'),
        ),
        migrations.AddField(
            model_name='band',
            name='manager',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='festivalapp.Employee'),
        ),
    ]
