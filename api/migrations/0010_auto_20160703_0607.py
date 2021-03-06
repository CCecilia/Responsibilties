# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-03 06:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20160703_0544'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceoption',
            name='values',
            field=models.CharField(default='', max_length=254),
        ),
        migrations.AlterField(
            model_name='serviceoption',
            name='input_type',
            field=models.CharField(choices=[('RD', 'radio'), ('TX', 'text'), ('EM', 'email'), ('NM', 'number'), ('CB', 'checkbox')], default='TX', max_length=2),
        ),
    ]
