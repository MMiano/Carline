# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-10 16:06
from __future__ import unicode_literals

from django.db import migrations, models
import mainapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20180213_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='videofile',
            field=models.FileField(blank=True, null=True, upload_to=mainapp.models.upload_location),
        ),
    ]
