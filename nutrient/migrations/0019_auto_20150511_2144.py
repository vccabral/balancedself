# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0018_auto_20150511_0510'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nutrient',
            options={'ordering': ['importance', 'name']},
        ),
        migrations.AddField(
            model_name='nutrient',
            name='importance',
            field=models.IntegerField(default=1),
        ),
    ]
