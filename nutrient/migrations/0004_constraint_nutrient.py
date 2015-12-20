# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0003_auto_20150429_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='constraint',
            name='nutrient',
            field=models.ForeignKey(default=1, to='nutrient.Nutrient'),
            preserve_default=False,
        ),
    ]
