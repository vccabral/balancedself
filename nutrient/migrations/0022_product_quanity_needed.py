# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0021_auto_20151218_2259'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quanity_needed',
            field=models.CharField(default=b'', max_length=200, blank=True),
        ),
    ]
