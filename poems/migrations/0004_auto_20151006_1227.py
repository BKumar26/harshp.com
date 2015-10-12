# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poems', '0003_auto_20150908_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poem',
            name='slug',
            field=models.CharField(unique=True, max_length=250),
        ),
    ]
