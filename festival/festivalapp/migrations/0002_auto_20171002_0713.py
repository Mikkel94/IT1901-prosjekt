# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-02 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festivalapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scene',
            name='id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
        ),
    ]