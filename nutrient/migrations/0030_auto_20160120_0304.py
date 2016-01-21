# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_product_tags(apps, schema_editor):
	Product = apps.get_model("nutrient", "Product")
	Tag = apps.get_model("nutrient", "Tag")

	tags = [
		"vegan", # 0
		"vegetarian", # 1
		"seafood", # 2
		"fruit", # 3
		"organic", # 4
		"wild caught", # 5
		"canned", # 6
		"red meat", # 7
		"dairy", # 8
		"nut", # 9
		"mushrooms", #10,
		"plant", #11
		"meat", #12
		"eggs", #13
	]

	for tag in tags:
		Tag(name=tag).save()

	vegatable = [0,1,11]
	fruit = [0,1,3,11]
	wild_seafood = [2,5,12]
	farmed_seafood = [2,12]
	red_meat = [7,12]
	eggs = [13,8]
	dairy = [8,]
	chicken = [12,]
	organic_chicken = [12, 4]
	nuts = [0,1,9]
	mushrooms = [0,1,10,11]
	canned_seafood = [2,5,12,6]

	product_raw_list = [
		["clementines",fruit],
		["oranges ",fruit],
		["gala apples",fruit],
		["Fuji apples",fruit],
		["Pink ladies",fruit],
		["Honey crisps",fruit],
		["Red delicious",fruit],
		["strawberries",fruit],
		["blueberries",fruit],
		["pomegranate wonderful variety",fruit],
		["cantaloupes",fruit],
		["gold kiwi",fruit],
		["apple pears",fruit],
		["pineapple",fruit],
		["Golden Mellon",fruit],
		["honeydew",fruit],
		["Red grape less seeds",fruit],
		["black seedless grapes",fruit],
		["green seedless grapes",fruit],
		["blackberry",fruit],
		["raspberries",fruit],
		["grapefruit large premium",fruit],
		["mangos",fruit],
		["gold potatoes",vegatable],
		["baking potatoes",vegatable],
		["sweet potatoes",vegatable],
		["dates",fruit],
		["lemons",fruit],
		["avocados",fruit],
		["sweet red onions",vegatable],
		["Peru sweet onions",vegatable],
		["table carrots",vegatable],
		["red rooster potatoes",vegatable],
		["plantains",fruit],
		["bananas",fruit],
		["celery hearts",vegatable],
		["bag asparagus",vegatable],
		["romaine hearts",vegatable],
		["baby spinach",vegatable],
		["spinach",vegatable],
		["large white mushrooms",mushrooms],
		["baby portobello mushrooms",mushrooms],
		["sweet corn",vegatable],
		["Brussels sprouts",vegatable],
		["beefsteak tomatoes",vegatable],
		["English green house grown cucumbers",vegatable],
		["garlic",vegatable],
		["grape tomatoes",vegatable],
		["tomato medley green house grown",vegatable],
		["Campari tomatoes",vegatable],
		["Roma tomatoes",vegatable],
		["smoked sockeye salmon",wild_seafood],
		["Norwegian smoked salmon",wild_seafood],
		["chicken breasts",chicken],
		["organic chicken breast",organic_chicken],
		["farmed Atlantic salmon",farmed_seafood],
		["wild caught Atlantic cod",wild_seafood],
		["fresh farmed steelhead",farmed_seafood],
		["wild caught haddock",wild_seafood],
		["farm fresh catfish",farmed_seafood],
		["fresh farmed tilapia",farmed_seafood],
		["farmed black mega shrimp",farmed_seafood],
		["farmed mega shrimp",farmed_seafood],
		["organic ground beef",red_meat],
		["88% lean ground beef",red_meat],
		["frozen patties beef",red_meat],
		["frozen broccoli florets",vegatable],
		["frozen French green beans.",vegatable],
		["Alaskan salmon burgers",wild_seafood],
		["frozen Atlantic cod",wild_seafood],
		["flounder fillets",wild_seafood],
		["tillapia loins",wild_seafood],
		["cooked shrimp",wild_seafood],
		["raw tail on",wild_seafood],
		["cooked tail off",wild_seafood],
		["wild Alaskian salmon",wild_seafood],
		["raw sea scallops",farmed_seafood],
		["slides bacon",red_meat],
		["organic brown eggs",eggs],
		["large grade a eggs",eggs],
		["extra large eggs",eggs],
		["sharp cheddar",dairy],
		["unsalted butter",dairy],
		["skip jack tuna chunk light",canned_seafood],
		["almond butter",vegatable],
		["black beans",vegatable],
		["green beans",vegatable],
		["almonds",nuts],
		["walnuts",nuts],
		["pecans",nuts],
		["organic coconut oil",vegatable],
	]

	for product in product_raw_list:
		prod = Product.objects.get(name=product[0])
		tags_for_me = []
		for tag_index in product[1]:
			tag = Tag.objects.get(name=tags[tag_index])
			tags_for_me.append(tag)
		prod.tags.add(*tags_for_me)
		prod.save()

class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0029_auto_20160112_0728'),
    ]

    operations = [
    	migrations.RunPython(add_product_tags)
    ]
