# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0015_auto_20150505_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='nutritionfact',
            name='company_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='nutritionfact',
            name='from_manufacturer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='nutritionfact',
            name='from_trusted_unpaid_thirdparty',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='nutritionfact',
            name='from_user',
            field=models.BooleanField(default=True),
        ),
    ]
