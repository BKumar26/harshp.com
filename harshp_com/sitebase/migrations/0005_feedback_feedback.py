# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-13 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitebase', '0004_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='feedback',
            field=models.TextField(blank=True),
        ),
    ]
