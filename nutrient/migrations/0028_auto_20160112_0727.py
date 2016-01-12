# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0027_auto_20160108_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutritionfact',
            name='quantity',
            field=models.DecimalField(max_digits=12, decimal_places=3),
        ),
    ]
