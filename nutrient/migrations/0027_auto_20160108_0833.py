# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_default_sizes(apps, schema_editor):
	Product = apps.get_model("nutrient", "Product")

	prod = Product.objects.get(name="Bacon")
	prod.quantity = 0
	prod.max_quantity = 1
	prod.save()

	prod = Product.objects.get(name="Eggs")
	prod.quantity = 0
	prod.max_quantity = 3
	prod.save()

	prod = Product.objects.get(name="Grass-fed butter")
	prod.quantity = 0
	prod.max_quantity = 2
	prod.save()

	prod = Product.objects.get(name="Olive oil")
	prod.quantity = 0
	prod.max_quantity = 1
	prod.save()

	prod = Product.objects.get(name="Coconut oil")
	prod.quantity = 0
	prod.max_quantity = 1
	prod.save()

	prod = Product.objects.get(name="Beef")
	prod.quantity = 0
	prod.max_quantity = 3
	prod.save()

	prod = Product.objects.get(name="Chicken Breast")
	prod.quantity = 0
	prod.max_quantity = 3
	prod.save()


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0026_auto_20160108_0833'),
    ]

    operations = [
		migrations.RunPython(add_default_sizes),
    ]
