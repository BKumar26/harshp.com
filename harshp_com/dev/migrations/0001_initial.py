# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 18:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sitebase', '0003_auto_20160214_2024'),
    ]

    operations = [
        migrations.CreateModel(
            name='DevPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=128)),
                ('date_created', models.DateTimeField()),
                ('date_published', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(db_index=True, default=False, verbose_name='published')),
                ('short_description', models.CharField(max_length=150)),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('body_type', models.CharField(choices=[('default', 'textarea'), ('html', 'html'), ('markdown', 'markdown')], default='markdown', max_length=8)),
                ('body_text', models.TextField(blank=True)),
                ('body', models.TextField()),
                ('headerimage', models.URLField(blank=True, max_length=256, null=True)),
                ('highlight', models.BooleanField(db_index=True, default=False)),
                ('authors', models.ManyToManyField(to='sitebase.Author')),
            ],
            options={
                'verbose_name': 'dev post',
                'verbose_name_plural': 'dev posts',
            },
        ),
        migrations.CreateModel(
            name='DevSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=128)),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('section_type', models.CharField(choices=[('default', 'default'), ('res', 'resources'), ('guide', 'guides & tutorials'), ('discuss', 'discussions'), ('mystack', 'my stack'), ('project', 'projects')], db_index=True, default='default', max_length=8)),
            ],
            options={
                'verbose_name': 'dev section',
                'verbose_name_plural': 'dev sections',
                'ordering': ['title'],
            },
        ),
        migrations.AddField(
            model_name='devpost',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dev.DevSection'),
        ),
        migrations.AddField(
            model_name='devpost',
            name='tags',
            field=models.ManyToManyField(to='sitebase.Tag'),
        ),
    ]
