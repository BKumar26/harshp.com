# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-29 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lifeX', '0003_lifexexperiment_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lifexexperiment',
            name='rating',
            field=models.IntegerField(choices=[(5, 'SCORE-5'), (4, 'SCORE-4'), (3, 'SCORE-3'), (2, 'SCORE-2'), (1, 'SCORE-1'), (0, 'NONE')], default=0),
        ),
    ]
