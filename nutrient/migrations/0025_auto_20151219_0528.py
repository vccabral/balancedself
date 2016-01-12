# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import *

def add_conversion_factors(apps, schema_editor):
	Product = apps.get_model("nutrient", "Product")

	product_info = [
		("Beef", Decimal(3.99), "1 lbs"),
		("Eggs", Decimal(4.69), "18 Eggs"),
		("Chicken Breast", Decimal(5.49), "1 lbs"),
		("Bacon", Decimal(6.99), "1 lbs"),
		("Asparagus", Decimal(2.49), "1 lbs"),
		("Avocado", Decimal(1.25), "1 Avocado"),
		("Artichoke hearts", Decimal(3.99), "1 Artichoke"),
		("Brussels sprouts", Decimal(2.99), "1 lbs"),
		("Carrots", Decimal(1.79), "2 lbs"),
		("Spinach", Decimal(2.50), "376 grams"),
		("Celery", Decimal(1.89), "1 stalk"),
		("Broccoli", Decimal(3.99), "1 lbs"),
		("Zucchini", Decimal(1.69), "1 lbs"),
		("Cabbage", Decimal(2.55), "1 Cabbage"),
		("Peppers", Decimal(3.00), "2 Peppers"),
		("Cauliflower", Decimal(4.99), "1 Cauliflower"),
		("Eggplant", Decimal(1.99), "1 lbs"),
		("Sweet Potatoes", Decimal(5.00), "10 lbs"),
		("Coconut oil", Decimal(25.00), "750 mls Coconut Oil"),
		("Olive oil", Decimal(12.99), "750 mls Olive Oil"),
		("Grass-fed butter", Decimal(3.49), "1 lbs"),
		("Almonds", Decimal(5.99), "198 grams"),
		("Cashews", Decimal(4.99), "212 grams"),
		("Hazelnuts", Decimal(5.99), "226 grams"),
		("Pecans", Decimal(5.99), "226 grams"),
		("Pine nuts", Decimal(5.99), "113 grams"),
		("Pumpkin seeds", Decimal(2.99), "226 grams"),
		("Macadamia nuts", Decimal(100.00), "226 grams"),
		("Walnuts", Decimal(3.99), "212 grams"),
		("Apple", Decimal(1.99), "1 lbs"),
		("Blackberries", Decimal(4.99), "6 ounces"),
		("Papaya", Decimal(1.29), "1 lbs"),
		("Peaches", Decimal(100.00), "6 ounces"),
		("Plums", Decimal(100.00), "6 ounces"),
		("Mango", Decimal(1.25), "1 Mango"),
		("Blueberries", Decimal(3.50), "6 ounces"),
		("Grapes", Decimal(3.49), "1 lbs"),
		("Lemon", Decimal(1.50), "2 lemons"),
		("Strawberries", Decimal(100.00), "6 ounces"),
		("Watermelon", Decimal(100.00), "6 ounces"),
		("Lime", Decimal(1.00), "4 Limes"),
		("Raspberries", Decimal(3.99), "6 ounces"),
		("Cantaloupe", Decimal(3.99), "1 Cantaloupe"),
		("Tangerine", Decimal(3.99), "5 lbs"),
		("Figs", Decimal(100.00), "6 ounces"),
		("Oranges", Decimal(1.0), "1 Orange"),
		("Canned Sockeye Salmon", Decimal(4.51), "1 Package of Salmon")
	]

	conversion_factor_db = {
		"1 lbs": 4.5359237,
		'6 ounces': 1.70097139, 
		'1 Mango': 2.07,
		'2 lemons': 2.16,
		'750 mls Olive Oil': 7.5,
		'1 Avocado': 2.01,
		'212 grams': 2.12, 
		'1 stalk': 0.4, 
		'1 Cauliflower': 5.75, 
		'113 grams': 1.13, 
		'1 Cantaloupe': 8.14, 
		'2 Peppers': 1.19, 
		'1 Cabbage': 9.08, 
		'5 lbs': 4.5359237*5, 
		'750 mls Coconut Oil': 7.5, 
		'1 Orange': 1.31, 
		'10 lbs': 4.5359237*10, 
		'376 grams': 3.76, 
		'1 Artichoke': 1.28, 
		'2 lbs': 4.5359237*2, 
		'4 Limes': 0.67*4, 
		'198 grams': 1.98, 
		'18 Eggs': 0.5*18, 
		'226 grams': 2.26,
		'1 Package of Salmon': 0.56
	}

	for product_name, price, package_size in product_info:
		cur_product = Product.objects.get(name=product_name)

		cur_product.price = price
		cur_product.quanity_needed = package_size
		cur_product.conversion_factor = conversion_factor_db[package_size]

		for nutrition_fact in cur_product.nutrition_facts.all():
			nutrition_fact.quantity = nutrition_fact.quantity * Decimal(cur_product.conversion_factor)
			nutrition_fact.save()
		
		cur_product.has_been_converted = True
		cur_product.save()

	# print(1/0)


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0024_auto_20151219_0528'),
    ]

    operations = [
    	migrations.RunPython(add_conversion_factors),
    ]

