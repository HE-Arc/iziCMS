# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-06 12:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iziCMSapp', '0007_auto_20170306_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='link',
            field=models.URLField(default=''),
        ),
    ]
