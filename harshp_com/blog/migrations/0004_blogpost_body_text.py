# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-20 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160214_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='body_text',
            field=models.TextField(blank=True),
        ),
    ]
