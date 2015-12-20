from django.core.management.base import BaseCommand, CommandError
from nutrient import models

class Command(BaseCommand):
	def handle(self, *args, **options):
		for raw_data in models.RawData.objects.all():
			product_exists_query = models.Product.objects.filter(name=raw_data.product)
			unit_exists_query = models.UnitOfMeasure.objects.filter(name=raw_data.unit)
			nutrient_exists_query = models.Nutrient.objects.filter(name=raw_data.nutrient)
			nutrient_info_exists_query = models.NutritionFact.objects.filter(product__name=raw_data.product)

			if not product_exists_query.exists():
				cur_product = models.Product(name=raw_data.product,price=1)
				cur_product.save()
			else:
				cur_product = product_exists_query[0]

			if not unit_exists_query.exists():
				cur_unit = models.UnitOfMeasure(name=raw_data.unit)
				cur_unit.save()
			else:
				cur_unit = unit_exists_query[0]

			if not nutrient_exists_query.exists():
				cur_nutrient = models.Nutrient(name=raw_data.nutrient, unit=cur_unit, minimum_scale=0, maximum_scale=100, number_of_ticks=100)
				cur_nutrient.save()
			else:
				cur_nutrient = nutrient_exists_query[0]

			if not nutrient_info_exists_query.exists():
				nutrient_info_exists_query.delete()
			nutrient_info = models.NutritionFact(product=cur_product, nutrient=cur_nutrient, quantity=raw_data.name)
			nutrient_info.save()