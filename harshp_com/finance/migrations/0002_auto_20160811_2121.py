# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-11 20:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='date_end',
            field=models.DateField(blank=True, db_index=True),
        ),
    ]
