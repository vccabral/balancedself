# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0004_constraint_nutrient'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('unit', models.CharField(max_length=200)),
                ('product', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='constraint',
            name='standard',
            field=models.ForeignKey(related_name='constraints', to='nutrient.Standard'),
        ),
        migrations.AlterField(
            model_name='nutritionfact',
            name='product',
            field=models.ForeignKey(related_name='nutrition_facts', to='nutrient.Product'),
        ),
    ]
