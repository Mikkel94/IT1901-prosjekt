# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 22:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('festivalapp', '0003_auto_20170918_0749'),
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, null=True)),
                ('members', models.IntegerField(default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('bands', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='festivalapp.Band')),
            ],
        ),
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='concert',
            name='scenes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='festivalapp.Scene'),
        ),
    ]
