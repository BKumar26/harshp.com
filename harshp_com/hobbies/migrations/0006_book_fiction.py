# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-14 20:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hobbies', '0005_auto_20170924_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='fiction',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
