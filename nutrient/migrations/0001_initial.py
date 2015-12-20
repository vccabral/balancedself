# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constraint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.DecimalField(max_digits=9, decimal_places=3)),
                ('equal_or_greater', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Nutrient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('minimum_scale', models.DecimalField(max_digits=9, decimal_places=3)),
                ('maximum_scale', models.DecimalField(max_digits=9, decimal_places=3)),
                ('number_of_ticks', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NutritionFact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.DecimalField(max_digits=9, decimal_places=3)),
                ('nutrient', models.ForeignKey(to='nutrient.Nutrient')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Standard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UnitOfMeasure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(to='nutrient.Tag'),
        ),
        migrations.AddField(
            model_name='nutritionfact',
            name='product',
            field=models.ForeignKey(to='nutrient.Product'),
        ),
        migrations.AddField(
            model_name='nutrient',
            name='unit',
            field=models.ForeignKey(to='nutrient.UnitOfMeasure'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='standard',
            field=models.ForeignKey(to='nutrient.Standard'),
        ),
    ]
