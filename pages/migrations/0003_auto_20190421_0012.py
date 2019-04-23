# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-21 00:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20190419_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='smuser',
            name='storyboard_last_updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='smuser',
            name='active_storyboard_id',
            field=models.IntegerField(default=1),
        ),
    ]
