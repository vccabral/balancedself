# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_product_tags(apps, schema_editor):
	Product = apps.get_model("nutrient", "Product")
	Tag = apps.get_model("nutrient", "Tag")

	tags = [
		"farmed fished",
	]

	for tag in tags:
		Tag(name=tag).save()

	farmed_fish = [0,]

	product_raw_list = [
		["farmed Atlantic salmon",farmed_fish],
		["fresh farmed steelhead",farmed_fish],
		["farm fresh catfish",farmed_fish],
		["fresh farmed tilapia",farmed_fish],
		["farmed black mega shrimp",farmed_fish],
		["farmed mega shrimp",farmed_fish],
	]

	for product in product_raw_list:
		prod = Product.objects.get(name=product[0].upper())
		tags_for_me = []
		for tag_index in product[1]:
			tag = Tag.objects.get(name=tags[tag_index])
			tags_for_me.append(tag)
		prod.tags.add(*tags_for_me)
		prod.save()



class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0031_auto_20160120_1524'),
    ]

    operations = [
		migrations.RunPython(add_product_tags)
    ]
