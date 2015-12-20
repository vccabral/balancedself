# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0005_auto_20150430_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawdata',
            name='nutrient',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
