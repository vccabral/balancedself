# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0011_auto_20150505_0430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutrient',
            name='name',
            field=models.CharField(unique=True, max_length=200),
        ),
    ]
