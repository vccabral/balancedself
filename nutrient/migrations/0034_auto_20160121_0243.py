# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_product_tags(apps, schema_editor):
	Tag = apps.get_model("nutrient", "Tag")
	Product = apps.get_model("nutrient", "Product")

	tags = [
		"starch",
	]

	for tag in tags:
		Tag(name=tag).save()

	starch = [0,]

	product_raw_list = [
		["gold potatoes",starch],
		["baking potatoes",starch],
		["sweet potatoes",starch],
		["red rooster potatoes",starch],
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
        ('nutrient', '0033_auto_20160121_0210'),
    ]

    operations = [
		migrations.RunPython(add_product_tags)
    ]
