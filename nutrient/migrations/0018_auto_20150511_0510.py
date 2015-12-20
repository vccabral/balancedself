# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0017_product_confirmed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='constraint',
            options={'ordering': ['nutrient']},
        ),
        migrations.AlterUniqueTogether(
            name='constraint',
            unique_together=set([('standard', 'nutrient')]),
        ),
    ]
