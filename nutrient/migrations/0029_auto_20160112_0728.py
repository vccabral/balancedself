# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import urllib2
import re
import demjson
from bs4 import BeautifulSoup
from decimal import *

def page_to_array_of_nutrient_info(url, Nutrient):

	nutrients = ["Calories","Fat","Carbohyrates","Fiber","Sugars","Protein","Vitamin A","Vitamin C","Vitamin D","Vitamin E","Vitamin K","Thiamin","Riboflavin","Niacin","Vitamin B6","Folate","Vitamin B12","Pantothenic Acid","Choline","Betaine","Calcium","Iron","Magnesium","Phosphorus","Potassium","Sodium","Zinc","Copper","Manganese","Selenium","Cholesterol"]
	nutrients_id = [0,14,4,5,7,77,97,100,101,102,103,107,108,109,110,111,115,116,143,144,117,118,119,120,121,122,123,124,125,126,72]
	response = urllib2.urlopen(url)
	html_doc = response.read()
	soup = BeautifulSoup(html_doc, 'html.parser')
	script = str(soup.find_all("script")[36].string)
	serving = soup.find("select",  {"name": "serving"}).findAll("option")[0].contents[0]

	p = re.compile('foodNutrients = ([^;]+);')
	m = p.search(script)
	food_nutrients = str(m.groups(0)[0]) 
	stocks = demjson.decode(food_nutrients)

	# nutrient_info, product_unit, raw_joson
	nutrient_info = [float(stocks["NUTRIENT_"+str(nutrients_id[nutrients.index(nutrient)])]) if stocks["NUTRIENT_"+str(nutrients_id[nutrients.index(nutrient)])] != "~" else 0 for nutrient in nutrients] 
	return nutrient_info, serving, stocks

def to_grams(num, units):
	if units == "lbs":
		return str(453.592 * float(num))
	elif units == "ounces":
		return str(28.3495 * float(num))
	elif units == "cucumber":
		return str(301 * float(num))
	elif units == "cob":
		return str(63 * float(num))
	elif units == "qts":
		return str(864.59 * float(num))
	elif units == "cantaloupe":
		return str(552 * float(num))
	elif units == "pineapple":
		return str(1002 * float(num))
	elif units == "Mellon":
		return str(552 * float(num))
	elif units == "honeydew":
		return str(1280 * float(num))
	elif units == "mango":
		return str(200 * float(num))
	elif units == "avocado":
		return str(201 * float(num))
	elif units == "celery heart":
		return str(40 * float(num))
	elif units == "romain heart":
		return str(628 * float(num))
	elif units == "cucumber":
		return str(301 * float(num))
	# elif units == "mixed bell pepper":
	# 	return "200"
	# elif units == "red bell pepper":
	# 	return "200"
	elif units == "dozen brown eggs":
		return str(44 * 12 * float(num))
	elif units == "12 large egg":		
		return str(50 * 12 * float(num))
	elif units == "12 extra large egg":		
		return str(56 * 12 * float(num))
	return None

def add_costco_products(apps, schema_editor):
	Product = apps.get_model("nutrient", "Product")
	NutritionFact = apps.get_model("nutrient", "NutritionFact")
	Nutrient = apps.get_model("nutrient", "Nutrient")
	Product.objects.all().delete()

	product_raw_list = [
		["5","lbs","clementines","5.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/9169/2"],
		["13","lbs","oranges ","11.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1969/2"],
		["5.5","lbs","gala apples","7.49","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1809/2"],
		["5.5","lbs","Fuji apples","8.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1809/2"],
		["5.5","lbs","Pink ladies","8.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1809/2"],
		["5.5","lbs","Honey crisps","16.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1809/2"],
		["10","lbs","Red delicious","8.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1809/2"],
		["2","lbs","strawberries","5.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/2064/2"],
		["18","ounces","blueberries","4.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1851/2"],
		["8","lbs","pomegranate wonderful variety","12.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/2038/2"],
		["3","cantaloupe","cantaloupes","5.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1954/2"],
		["2","lbs","gold kiwi","4.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1934/2"],
		["3.5","lbs","apple pears","6.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/2005/2"],
		["1","pineapple","pineapple","2.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/7350/2"],
		["1","Mellon","Golden Mellon","3.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1954/2"],
		["1","honeydew","honeydew","3.79","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1954/2"],
		["4","lbs","Red grape less seeds","9.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1920/2"],
		["4","lbs","black seedless grapes","8.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1920/2"],
		["4","lbs","green seedless grapes","9.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1920/2"],
		["18","ounces","blackberry","4.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1848/2"],
		["12","ounces","raspberries","4.49","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/2053/2"],
		["8","lbs","grapefruit large premium","6.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1908/2"],
		["6","mango","mangos","7.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1952/2"],
		["15","lbs","gold potatoes","8.79","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2546/2"],
		["20","lbs","baking potatoes","7.49","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2546/2"],
		["10","lbs","sweet potatoes","7.99","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2666/2"],
		["2","lbs","dates","8.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/7348/2"],
		["5","lbs","lemons","7.79","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1937/2"],
		["6","avocado","avocados","4.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1843/2"],
		["8","lbs","sweet red onions","7.99","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2501/2"],
		["5","lbs","Peru sweet onions","3.99","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2501/2"],
		["2","lbs","table carrots","6.49","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2383/2"],
		["10","lbs","red rooster potatoes","6.99","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2501/2"],
		["5","lbs","plantains","2.99","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/2030/2"],
		["3","lbs","bananas","1.39","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1846/2"],
		["4","celery heart","celery hearts","3.79","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2396/2"],
		["2.25","lbs","bag asparagus","8.99","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2311/2"],
		["5","romain heart","romaine hearts","3.49","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2475/2"],
		["1","lbs","baby spinach","4.49","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2626/2"],
		["2.5","lbs","spinach","4.99","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2626/2"],
		["24","ounces","large white mushrooms","3.99","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2482/2"],
		["24","ounces","baby portobello mushrooms","3.99","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/9170/2"],
		["8","cob","sweet corn","5.49","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2415/2"],
		["2","lbs","Brussels sprouts","4.49","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2362/2"],
		["5","lbs","beefsteak tomatoes","6.99","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2682/2"],
		["3","cucumber","English green house grown cucumbers","3.99","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2439/2"],
		["2","lbs","garlic","5.99","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2446/2"],
		# ["6","mixed bell pepper","mixed bell peppers","6.99",""],
		# ["6","red bell pepper","red bell peppers","6.49",""],
		["2","lbs","grape tomatoes","5.99","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2682/2"],
		["2","lbs","tomato medley green house grown","5.49","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2682/2"],
		["2","lbs","Campari tomatoes","4.99","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2682/2"],
		["2","lbs","Roma tomatoes","4.99","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2682/2"],
		["1","lbs","smoked sockeye salmon","14.89","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/4111/2"],
		["0.75","lbs","Norwegian smoked salmon","8.99","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/4102/2"],
		["9.52","lbs","chicken breasts","28.46","http://nutritiondata.self.com/facts/poultry-products/701/2"],
		["3.48","lbs","organic chicken breast","20.85","http://nutritiondata.self.com/facts/poultry-products/701/2"],
		["1.89","lbs","farmed Atlantic salmon","16.99","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/4102/2"],
		["2.19","lbs","wild caught Atlantic cod","17.50","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/4041/2"],
		["1.43","lbs","fresh farmed steelhead","10.00","http://nutritiondata.self.com/facts/ethnic-foods/9997/2"],
		["2","lbs","wild caught haddock","17.98","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/4059/2"],
		["2.23","lbs","farm fresh catfish","15.59","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/4256/2"],
		["2.48","lbs","fresh farmed tilapia","12.38","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/9243/2"],
		# ["2","lbs","lobster tails","26.99",""],
		["4","lbs","farmed black mega shrimp","49.99","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/4172/2"],
		["1.87","lbs","farmed mega shrimp","24.29","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/4172/2"],
		["4","lbs","organic ground beef","21.99","http://nutritiondata.self.com/facts/beef-products/10526/2"],
		["5.18","lbs","88% lean ground beef","17.56","http://nutritiondata.self.com/facts/beef-products/6193/2"],
		["10","lbs","frozen patties beef","25.99","http://nutritiondata.self.com/facts/beef-products/6193/2"],
		["4","lbs","frozen broccoli florets","6.89","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2816/2"],
		["5","lbs","frozen French green beans.","6.39","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2341/2"],
		["3","lbs","Alaskan salmon burgers","14.99","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/4102/2"],
		["2","lbs","frozen Atlantic cod","12.99","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/4041/2"],
		["2","lbs","flounder fillets","10.29","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/4054/2"],
		["2.5","lbs","tillapia loins","14.99","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/9243/2"],
		# ["3","lbs","wild mahi mahi","19.99",""],
		["2","lbs","cooked shrimp","16.99","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/4174/2"],
		["2","lbs","raw tail on","13.99","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/4172/2"],
		["2","lbs","cooked tail off","14.89","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/4172/2"],
		["3","lbs","wild Alaskian salmon","26.99","http://nutritiondata.self.com/facts/ethnic-foods/9971/2"],
		["2","lbs","raw sea scallops","34.99","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2637/2"],
		["4","lbs","slides bacon","14.99","http://nutritiondata.self.com/facts/pork-products/2208/2"],
		["2","dozen brown eggs","organic brown eggs","6.99","http://nutritiondata.self.com/facts/dairy-and-egg-products/112/2"],
		["7.5","12 large egg","large grade a eggs","9.59","http://nutritiondata.self.com/facts/dairy-and-egg-products/112/2"],
		["3","12 extra large egg","extra large eggs","3.99","http://nutritiondata.self.com/facts/dairy-and-egg-products/112/2"],
		["2","lbs","sharp cheddar","4.99","http://nutritiondata.self.com/facts/dairy-and-egg-products/8/2"],
		["4","lbs","unsalted butter","9.99","http://nutritiondata.self.com/facts/fats-and-oils/7584/2"],
		# ["4","lbs","Greek yogurt","5.89",""],
		# ["3.5","lbs","solid white albacore canned","10.89",""],
		# ["0.375","lbs","roasted seaweed","8.39",""],
		["5.25","lbs","skip jack tuna chunk light","13.49","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/4146/2"],
		["1.6875","lbs","almond butter","11.99","http://nutritiondata.self.com/facts/nut-and-seed-products/3183/2"],
		# ["2.75","lbs","raw unfiltered honey","14.79",""],
		# ["4.5","lbs","clover honey","12.99",""],
		["10","lbs","black beans","7.79","http://nutritiondata.self.com/facts/legumes-and-legume-products/4283/2"],
		# ["5.81","lbs","red kidney beans","4.69",""],
		# ["7.75","lbs","black beans","5.29","http://nutritiondata.self.com/facts/legumes-and-legume-products/4283/2"],
		# ["7.75","lbs","Goya chick peas","5.29","http://nutritiondata.self.com/facts/legumes-and-legume-products/4327/2"],
		["10.875","lbs","green beans","7.89","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2341/2"],
		# ["20","lbs","basmati rice","16.49","http://nutritiondata.self.com/facts/cereal-grains-and-pasta/5706/2"],
		# ["50","lbs","long grain rice","17.99","http://nutritiondata.self.com/facts/cereal-grains-and-pasta/5706/2"],
		["3","lbs","almonds","17.99","http://nutritiondata.self.com/facts/nut-and-seed-products/3085/2"],
		["3","lbs","walnuts","12.99","http://nutritiondata.self.com/facts/nut-and-seed-products/3137/2"],
		["2","lbs","pecans","12.49","http://nutritiondata.self.com/facts/nut-and-seed-products/3129/2"],
		["2.64","qts","organic coconut oil","24.59","http://nutritiondata.self.com/facts/fats-and-oils/508/2"]
	]

	for raw_product in product_raw_list:
		nutrient_info, product_unit, raw_joson = page_to_array_of_nutrient_info(raw_product[4], Nutrient)
		product = Product(
			name = raw_product[2],
			price = Decimal(raw_product[3]),
			confirmed = True,
			url = raw_product[4],
			quanity_as_listed = to_grams(raw_product[0], raw_product[1]),
			quantity = 0,
			max_quantity = 7
		)
		nutrients = ["Calories","Fat","Carbohyrates","Fiber","Sugars","Protein","Vitamin A","Vitamin C","Vitamin D","Vitamin E","Vitamin K","Thiamin","Riboflavin","Niacin","Vitamin B6","Folate","Vitamin B12","Pantothenic Acid","Choline","Betaine","Calcium","Iron","Magnesium","Phosphorus","Potassium","Sodium","Zinc","Copper","Manganese","Selenium","Cholesterol"]
		product.raw_data_body = raw_joson
		print(to_grams(raw_product[0], raw_product[1]))
		print(raw_product[0], raw_product[1])
		product.save()
        

		needed_quantity = float(product.quanity_as_listed) / 100.0

		for nutrient, quantity in zip(nutrients, nutrient_info):
			NutritionFact.objects.create(
				product = product, 
				nutrient_id = Nutrient.objects.get(name=nutrient).id,
				quantity = round(quantity * needed_quantity, 3)
			)



class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0028_auto_20160112_0727'),
    ]

    operations = [
		migrations.RunPython(add_costco_products),
    ]
