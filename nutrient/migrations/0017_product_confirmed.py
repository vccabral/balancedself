# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0016_auto_20150505_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
