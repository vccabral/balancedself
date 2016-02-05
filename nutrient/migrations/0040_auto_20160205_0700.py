# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def new_nutrient_settings(apps, schema_editor):
	Nutrient = apps.get_model("nutrient", "Nutrient")
	Constraint = apps.get_model("nutrient", "Constraint")
	Standard = apps.get_model("nutrient", "Standard")

	keto = Standard.objects.get(name="Keto")
	us_rdis = Standard.objects.get(name="US RDIs")

	nutrients = [
		["Choline",550,550],
		["Niacin",16,16],
		["Riboflavin",1.3,1.3],
		["Vitamin B12",2.4,2.4],
		["Vitamin B6",1.3,1.3],
		["Vitamin D",200,200],
		["Vitamin E",15,15],
		["Copper",0.9,0.9],
		["Iron",8,8],
		["Manganese",2.3,2.3],
		["Selenium",55,55],
	]

	for nutrient in nutrients:
		name = nutrient[0]
		nutrient_obj = Nutrient.objects.get(name=name)

		constraint_us_rdis = Constraint.objects.get(standard=us_rdis, nutrient=nutrient_obj)
		constraint_us_rdis.quantity = nutrient[1]
		constraint_us_rdis.save()

		constraint_keto = Constraint.objects.get(standard=keto, nutrient=nutrient_obj)
		constraint_keto.quantity = nutrient[2]
		constraint_keto.save()

	nutrients = [
		["Sodium",3000,None],
		["Cholesterol",300,None],
	]
	
	for nutrient in nutrients:
		name = nutrient[0]
		nutrient_obj = Nutrient.objects.get(name=name)

		constraint_us_rdis = Constraint.objects.get(standard=us_rdis, nutrient=nutrient_obj)
		constraint_us_rdis.max_quantity = nutrient[1]
		constraint_us_rdis.save()

		constraint_keto = Constraint.objects.get(standard=keto, nutrient=nutrient_obj)
		constraint_keto.max_quantity = nutrient[2]
		constraint_keto.save()


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0039_auto_20160131_2107'),
    ]

    operations = [
		migrations.RunPython(new_nutrient_settings)
    ]
