# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-03 06:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20160703_0607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceoption',
            name='placeholder',
            field=models.CharField(blank=True, default='', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='serviceoption',
            name='values',
            field=models.CharField(blank=True, default='', max_length=254, null=True),
        ),
    ]