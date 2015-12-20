# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0013_auto_20150505_0526'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='constraint',
            unique_together=set([]),
        ),
    ]
