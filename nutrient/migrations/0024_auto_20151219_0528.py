# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0023_auto_20151219_0519'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='conversion_factor',
            field=models.DecimalField(default=0, max_digits=12, decimal_places=5),
        ),
        migrations.AddField(
            model_name='product',
            name='has_been_converted',
            field=models.BooleanField(default=False),
        ),
    ]
