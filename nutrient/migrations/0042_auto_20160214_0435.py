# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def change_fish_price(apps, schema_editor):
	Product = apps.get_model("nutrient", "Product")
	fish = Product.objects.get(name="FRESH FARMED STEELHEAD")
	fish.price = 20.0
	fish.save()

class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0041_product_custom_span'),
    ]

    operations = [
		migrations.RunPython(change_fish_price)
    ]
