# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-02 08:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('festivalapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='band',
            name='light_needs',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='band',
            name='manager',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='festivalapp.Employee'),
        ),
        migrations.AddField(
            model_name='band',
            name='sound_needs',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='scene',
            name='id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='scene',
            name='name',
            field=models.CharField(default='Scene', max_length=50),
        ),
    ]
