# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-03 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20160703_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optioninput',
            name='input_type',
            field=models.CharField(choices=[('radio', 'radio'), ('text', 'text'), ('email', 'email'), ('number', 'number'), ('checkbox', 'checkbox'), ('hidden', 'hidden')], default='text', max_length=25),
        ),
    ]