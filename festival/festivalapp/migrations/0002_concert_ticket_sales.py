# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-26 10:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festivalapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='concert',
            name='ticket_sales',
            field=models.IntegerField(default=0),
        ),
    ]
