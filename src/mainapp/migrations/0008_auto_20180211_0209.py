# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-10 23:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_auto_20180210_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionitem',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Product'),
        ),
    ]
