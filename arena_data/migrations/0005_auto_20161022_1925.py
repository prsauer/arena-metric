# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-22 19:25
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('arena_data', '0004_auto_20161007_0009'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='data_3v3',
            managers=[
                ('fresh', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='pulldatamodel',
            managers=[
            ],
        ),
    ]