# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_product_tags(apps, schema_editor):
	Product = apps.get_model("nutrient", "Product")
	Tag = apps.get_model("nutrient", "Tag")

	tags = [
		"natural", # 0
		"processed", # 1
	]

	for tag in tags:
		Tag(name=tag).save()

	natural = [0,]
	processed = [1,]

	product_raw_list = [
		["clementines",natural],
		["oranges ",natural],
		["gala apples",natural],
		["Fuji apples",natural],
		["Pink ladies",natural],
		["Honey crisps",natural],
		["Red delicious",natural],
		["strawberries",natural],
		["blueberries",natural],
		["pomegranate wonderful variety",natural],
		["cantaloupes",natural],
		["gold kiwi",natural],
		["apple pears",natural],
		["pineapple",natural],
		["Golden Mellon",natural],
		["honeydew",natural],
		["Red grape less seeds",natural],
		["black seedless grapes",natural],
		["green seedless grapes",natural],
		["blackberry",natural],
		["raspberries",natural],
		["grapefruit large premium",natural],
		["mangos",natural],
		["gold potatoes",natural],
		["baking potatoes",natural],
		["sweet potatoes",natural],
		["dates",natural],
		["lemons",natural],
		["avocados",natural],
		["sweet red onions",natural],
		["Peru sweet onions",natural],
		["table carrots",natural],
		["red rooster potatoes",natural],
		["plantains",natural],
		["bananas",natural],
		["celery hearts",natural],
		["bag asparagus",natural],
		["romaine hearts",natural],
		["baby spinach",natural],
		["spinach",natural],
		["large white mushrooms",natural],
		["baby portobello mushrooms",natural],
		["sweet corn",natural],
		["Brussels sprouts",natural],
		["beefsteak tomatoes",natural],
		["English green house grown cucumbers",natural],
		["garlic",natural],
		["grape tomatoes",natural],
		["tomato medley green house grown",natural],
		["Campari tomatoes",natural],
		["Roma tomatoes",natural],
		["smoked sockeye salmon",processed],
		["Norwegian smoked salmon",processed],
		["chicken breasts",processed],
		["organic chicken breast",natural],
		["farmed Atlantic salmon",processed],
		["wild caught Atlantic cod",natural],
		["fresh farmed steelhead",processed],
		["wild caught haddock",natural],
		["farm fresh catfish",processed],
		["fresh farmed tilapia",processed],
		["farmed black mega shrimp",processed],
		["farmed mega shrimp",processed],
		["organic ground beef",natural],
		["88% lean ground beef",processed],
		["frozen patties beef",processed],
		["frozen broccoli florets",natural],
		["frozen French green beans.",natural],
		["Alaskan salmon burgers",natural],
		["frozen Atlantic cod",natural],
		["flounder fillets",natural],
		["tillapia loins",natural],
		["cooked shrimp",natural],
		["raw tail on",natural],
		["cooked tail off",natural],
		["wild Alaskian salmon",natural],
		["raw sea scallops",natural],
		["slices bacon",processed],
		["organic brown eggs",natural],
		["large grade a eggs",processed],
		["extra large eggs",processed],
		["sharp cheddar",processed],
		["unsalted butter",processed],
		["skip jack tuna chunk light",processed],
		["almond butter",natural],
		["black beans",natural],
		["green beans",natural],
		["almonds",natural],
		["walnuts",natural],
		["pecans",natural],
		["organic coconut oil",natural],
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
        ('nutrient', '0030_auto_20160120_0304'),
    ]

    operations = [
		migrations.RunPython(add_product_tags)
    ]

