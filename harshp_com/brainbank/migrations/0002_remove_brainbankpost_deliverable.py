# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-04 21:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brainbank', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brainbankpost',
            name='deliverable',
        ),
    ]
