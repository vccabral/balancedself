# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0012_auto_20150505_0524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='standard',
            name='name',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name='nutritionfact',
            unique_together=set([('product', 'nutrient')]),
        ),
    ]
