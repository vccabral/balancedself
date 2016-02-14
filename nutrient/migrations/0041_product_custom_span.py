# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0040_auto_20160205_0700'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='custom_span',
            field=models.CharField(default=b'daily', max_length=50),
        ),
    ]
