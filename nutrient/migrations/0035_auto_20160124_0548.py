# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def new_nutrient_settings(apps, schema_editor):
	Nutrient = apps.get_model("nutrient", "Nutrient")
	Constraint = apps.get_model("nutrient", "Constraint")
	nutrient = Nutrient.objects.get(name="Cholesterol")
	for constraint in Constraint.objects.filter(nutrient=nutrient):
		constraint.quantity = 0
		constraint.max_quantity = 300
		constraint.save()

class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0034_auto_20160121_0243'),
    ]

    operations = [
		migrations.RunPython(new_nutrient_settings)
    ]
