# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-11 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iziCMSapp', '0013_auto_20170411_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='root_folder',
            field=models.CharField(default='/', max_length=200),
        ),
    ]