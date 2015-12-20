# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import urllib2
import re
import demjson
from bs4 import BeautifulSoup
from django.db import migrations, models

def page_to_array_of_nutrient_info(url):
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


def create_advanced_data(apps, schema_editor):
    from django.db import models, migrations

    Standard = apps.get_model("nutrient", "Standard")
    Constraint = apps.get_model("nutrient", "Constraint")
    Tag = apps.get_model("nutrient", "Tag")
    Product = apps.get_model("nutrient", "Product")
    NutritionFact = apps.get_model("nutrient", "NutritionFact")
    Nutrient = apps.get_model("nutrient", "Nutrient")

    model_list = [Standard, Constraint, Tag, Product, NutritionFact]
    for model in model_list:
    	model.objects.all().delete()

    usrdi = Standard(name="US RDIs")
    usrdi.save()

    nutrients = [
        ("Calories", 2000, 3000),
        ("Fat", 65, None),
        ("Carbohyrates", 300, None),
        ("Fiber", 25, None),
        ("Sugars", 0, None),
        ("Protein", 50, None),
        ("Vitamin A", 5000, None),
        ("Vitamin C", 60, None),
        ("Vitamin D", 400, None),
        ("Vitamin E", 27, None),
        ("Vitamin K", 80, None),
        ("Thiamin", 1.5, None),
        ("Riboflavin", 1.7, None),
        ("Niacin", 20, None),
        ("Vitamin B6", 2, None),
        ("Folate", 400, None),
        ("Vitamin B12", 6, None),
        ("Pantothenic Acid", 10, None),
        ("Choline", 3400, None),
        ("Betaine", 0.3, None),
        ("Calcium", 1000, None),
        ("Iron", 18, None),
        ("Magnesium", 400, None),
        ("Phosphorus", 1000, None),
        ("Potassium", 3500, None),
        ("Sodium", 2400, None),
        ("Zinc", 15, None),
        ("Copper", 2, None),
        ("Manganese", 2, None),
        ("Selenium", 7, None),
        ("Cholesterol", 300, None)
    ]


    for nutrient, min_quantity, max_quantity in nutrients:
    	new_contraint = Constraint(
            standard = usrdi,
            quantity = min_quantity,
            max_quantity = max_quantity
        )
        new_contraint.nutrient = Nutrient.objects.get(name=nutrient)
        new_contraint.save()

    keto = Standard(name="Keto")
    keto.save()

    nutrients = [
        ("Calories", 2000, None),
        ("Fat", 65, None),
        ("Carbohyrates", 0, 50),
        ("Fiber", 25, None),
        ("Sugars", 0, None),
        ("Protein", 50, None),
        ("Vitamin A", 5000, None),
        ("Vitamin C", 60, None),
        ("Vitamin D", 400, None),
        ("Vitamin E", 27, None),
        ("Vitamin K", 80, None),
        ("Thiamin", 1.5, None),
        ("Riboflavin", 1.7, None),
        ("Niacin", 20, None),
        ("Vitamin B6", 2, None),
        ("Folate", 400, None),
        ("Vitamin B12", 6, None),
        ("Pantothenic Acid", 10, None),
        ("Choline", 3400, None),
        ("Betaine", 0.3, None),
        ("Calcium", 1000, None),
        ("Iron", 18, None),
        ("Magnesium", 400, None),
        ("Phosphorus", 1000, None),
        ("Potassium", 3500, None),
        ("Sodium", 2400, None),
        ("Zinc", 15, None),
        ("Copper", 2, None),
        ("Manganese", 2, None),
        ("Selenium", 7, None),
        ("Cholesterol", 300, None)
    ]

    for nutrient, min_quantity, max_quantity in nutrients:
        new_contraint = Constraint(
            standard = keto,
            quantity = min_quantity,
            max_quantity = max_quantity
        )
        new_contraint.nutrient = Nutrient.objects.get(name=nutrient)
        new_contraint.save()

    # Product(name,price)
    # NutritionFact(product,nutrient,quantity)
    products = ["Beef","Eggs","Chicken Breast","Bacon","Asparagus","Avocado","Artichoke hearts","Brussels sprouts","Carrots","Spinach","Celery","Broccoli","Zucchini","Cabbage","Peppers","Cauliflower","Eggplant","Sweet Potatoes","Coconut oil","Olive oil","Grass-fed butter","Almonds","Cashews","Hazelnuts","Pecans","Pine nuts","Pumpkin seeds","Macadamia nuts","Walnuts","Apple","Blackberries","Papaya","Peaches","Plums","Mango","Blueberries","Grapes","Lemon","Strawberries","Watermelon","Lime","Raspberries","Cantaloupe","Tangerine","Figs","Oranges"]
    product_urls = ["http://nutritiondata.self.com/facts/beef-products/10526/2","http://nutritiondata.self.com/facts/dairy-and-egg-products/111/2","http://nutritiondata.self.com/facts/poultry-products/696/2","http://nutritiondata.self.com/facts/pork-products/2208/2","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2311/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1843/2","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2307/2","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2362/2","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2383/2","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2626/2","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2396/2","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2356/2","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2639/2","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2371/2","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2536/2","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2390/2","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2443/2","http://nutritiondata.self.com/facts/vegetables-and-vegetable-products/2666/2","http://nutritiondata.self.com/facts/fats-and-oils/508/2","http://nutritiondata.self.com/facts/fats-and-oils/509/2","http://nutritiondata.self.com/facts/dairy-and-egg-products/0/2","http://nutritiondata.self.com/facts/nut-and-seed-products/3085/2","http://nutritiondata.self.com/facts/nut-and-seed-products/3095/2","http://nutritiondata.self.com/facts/nut-and-seed-products/3116/2","http://nutritiondata.self.com/facts/nut-and-seed-products/3129/2","http://nutritiondata.self.com/facts/nut-and-seed-products/3133/2","http://nutritiondata.self.com/facts/finfish-and-shellfish-products/4134/2","http://nutritiondata.self.com/facts/nut-and-seed-products/3123/2","http://nutritiondata.self.com/facts/nut-and-seed-products/3138/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1809/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1848/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1985/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1990/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/2032/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1952/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1851/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1919/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1936/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/2064/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/2072/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1942/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/2053/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1954/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1978/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1884/2","http://nutritiondata.self.com/facts/fruits-and-fruit-juices/1966/2"]
    product_prices = [(random.randrange(100, 250)/100.0) for product in products]
    nutrients = ["Calories","Fat","Carbohyrates","Fiber","Sugars","Protein","Vitamin A","Vitamin C","Vitamin D","Vitamin E","Vitamin K","Thiamin","Riboflavin","Niacin","Vitamin B6","Folate","Vitamin B12","Pantothenic Acid","Choline","Betaine","Calcium","Iron","Magnesium","Phosphorus","Potassium","Sodium","Zinc","Copper","Manganese","Selenium","Cholesterol"]

    for product, price, product_url in zip(products, product_prices, product_urls):
        
        nutrient_info, product_unit, raw_joson = page_to_array_of_nutrient_info(product_url)

        prod = Product(
            name = product, 
            price = price, 
            confirmed = True,
            url = product_url,
            quanity_as_listed = product_unit,
            raw_data_body = raw_joson
        )
        prod.save()

        for nutrient, quantity in zip(nutrients, nutrient_info):
            NutritionFact.objects.create(
                product = prod, 
                nutrient_id = Nutrient.objects.get(name=nutrient).id,
                quantity = quantity
            )


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0022_product_quanity_needed'),
    ]

    operations = [
    	migrations.RunPython(create_advanced_data),
    ]
