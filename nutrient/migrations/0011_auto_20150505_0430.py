# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0010_auto_20150505_0411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constraint',
            name='max_quantity',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=3, blank=True),
        ),
        migrations.AlterField(
            model_name='constraint',
            name='quantity',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=3, blank=True),
        ),
    ]
