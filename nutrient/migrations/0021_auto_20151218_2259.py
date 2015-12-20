# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.models import User


def create_basic_data(apps, schema_editor):
    User.objects.create_superuser('vccabral@gmail.com', 'vccabral@gmail.com', 'vccabral@gmail.com')
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    UnitOfMeasure = apps.get_model("nutrient", "UnitOfMeasure")
    Nutrient = apps.get_model("nutrient", "Nutrient")

    model_list = [Nutrient, UnitOfMeasure]
    for model in model_list:
    	model.objects.all().delete()

    # Units of Measure
    units = [
        {"name": "grams"},
        {"name": "milligrams"},
        {"name": "micrograms"},
        {"name": "Calories"},
        {"name": "IU"}
    ]

    for unit in units:
        UnitOfMeasure(**unit).save()

    grams = UnitOfMeasure.objects.get(name="grams")
    milligrams = UnitOfMeasure.objects.get(name="milligrams")
    micrograms = UnitOfMeasure.objects.get(name="micrograms")
    calories = UnitOfMeasure.objects.get(name="Calories")
    IU = UnitOfMeasure.objects.get(name="IU")

    # Nutrient
    nutrients = [
        {"name": "Calories", "unit": calories, "importance": 1},

        {"name": "Fat", "unit": grams, "importance": 2},
        {"name": "Carbohyrates", "unit": grams, "importance": 4},
        {"name": "Fiber", "unit": grams, "importance": 5},
        {"name": "Sugars", "unit": grams, "importance": 6},
        {"name": "Protein", "unit": grams, "importance": 3},

        {"name": "Vitamin A", "unit": IU, "importance": 7},
        {"name": "Vitamin C", "unit": milligrams, "importance": 7},
        {"name": "Vitamin D", "unit": IU, "importance": 7},
        {"name": "Vitamin E", "unit": milligrams, "importance": 7},
        {"name": "Vitamin K", "unit": micrograms, "importance": 7},
        {"name": "Thiamin", "unit": milligrams, "importance": 7},
        {"name": "Riboflavin", "unit": milligrams, "importance": 7},
        {"name": "Niacin", "unit": milligrams, "importance": 7},
        {"name": "Vitamin B6", "unit": milligrams, "importance": 7},
        {"name": "Folate", "unit": micrograms, "importance": 7},
        {"name": "Vitamin B12", "unit": micrograms, "importance": 7},
        {"name": "Pantothenic Acid", "unit": milligrams, "importance": 7},
        {"name": "Choline", "unit": milligrams, "importance": 7},
        {"name": "Betaine", "unit": milligrams, "importance": 7},

        {"name": "Calcium", "unit": milligrams, "importance": 8},
        {"name": "Iron", "unit": milligrams, "importance": 8},
        {"name": "Magnesium", "unit": milligrams, "importance": 8},
        {"name": "Phosphorus", "unit": milligrams, "importance": 8},
        {"name": "Potassium", "unit": milligrams, "importance": 8},
        {"name": "Sodium", "unit": milligrams, "importance": 8},
        {"name": "Zinc", "unit": milligrams, "importance": 8},
        {"name": "Copper", "unit": milligrams, "importance": 8},
        {"name": "Manganese", "unit": milligrams, "importance": 8},
        {"name": "Selenium", "unit": micrograms, "importance": 8},

        {"name": "Cholesterol", "unit": milligrams, "importance": 9},
    ]

    for nutrient in nutrients:
        Nutrient(**nutrient).save()


class Migration(migrations.Migration):

    dependencies = [
        ('nutrient', '0020_auto_20151218_2258'),
        ('sessions', '0001_initial'),
    ]

    operations = [
		migrations.RunPython(create_basic_data),
    ]
