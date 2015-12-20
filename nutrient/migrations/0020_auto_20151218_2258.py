# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0019_auto_20150511_2144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nutrient',
            options={'ordering': ['-importance', 'name']},
        ),
        migrations.AddField(
            model_name='product',
            name='quanity_as_listed',
            field=models.CharField(default=b'', max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='raw_data_body',
            field=models.CharField(default=b'', max_length=10000, blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='url',
            field=models.URLField(default=b'', blank=True),
        ),
    ]
