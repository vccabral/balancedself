# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0008_auto_20150505_0409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutrient',
            name='number_of_ticks',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
