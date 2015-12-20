# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0009_auto_20150505_0410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutrient',
            name='maximum_scale',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=3, blank=True),
        ),
        migrations.AlterField(
            model_name='nutrient',
            name='minimum_scale',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=3, blank=True),
        ),
    ]
