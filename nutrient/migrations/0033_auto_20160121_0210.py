# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_product_tags(apps, schema_editor):
	Constraint = apps.get_model("nutrient", "Constraint")

	new_max_constaints = [
		["Choline", 3000],
		["Vitamin A", 100000],
		["Vitamin C", 2000],
		["Vitamin D", 600],
		["Vitamin E", 1000],
		["Copper", 10],
		["Magnesium", 5000],
		["Phosphorus", 4000],
		["Potassium", 18000],
		["Selenium", 400],
		["Sodium", 2400.000],
		["Zinc", 40],
	]

	new_min_constaints = [
		["Sodium", 500.000],
	]

	for new_max_constaint_name, quantity in new_max_constaints:
		constraints_to_update = Constraint.objects.filter(nutrient__name=new_max_constaint_name)
		for constraint in constraints_to_update:
			constraint.max_quantity = quantity
			constraint.save()

	for new_min_constaint_name, quantity in new_min_constaints:
		constraints_to_update = Constraint.objects.filter(nutrient__name=new_min_constaint_name)
		for constraint in constraints_to_update:
			constraint.quantity = quantity
			constraint.save()




class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0032_auto_20160120_2343'),
    ]

    operations = [
		migrations.RunPython(add_product_tags)
    ]
