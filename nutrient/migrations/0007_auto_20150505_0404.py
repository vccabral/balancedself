# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0006_rawdata_nutrient'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nutrient',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='nutritionfact',
            options={'ordering': ['product__name']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='rawdata',
            options={'ordering': ['product', 'nutrient']},
        ),
        migrations.RemoveField(
            model_name='constraint',
            name='equal_or_greater',
        ),
        migrations.AddField(
            model_name='constraint',
            name='max_quantity',
            field=models.DecimalField(default=None, max_digits=9, decimal_places=3, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='constraint',
            name='quantity',
            field=models.DecimalField(max_digits=9, decimal_places=3, blank=True),
        ),
    ]
