# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0025_auto_20151219_0528'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nutrient',
            options={'ordering': ['importance', 'name', 'pk']},
        ),
        migrations.AddField(
            model_name='product',
            name='max_quantity',
            field=models.IntegerField(default=7),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
