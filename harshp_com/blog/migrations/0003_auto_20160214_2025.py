# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-14 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160214_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogseries',
            name='slug',
            field=models.SlugField(blank=True, max_length=150, unique=True),
        ),
    ]
