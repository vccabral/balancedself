from django.core.management.base import BaseCommand, CommandError
from nutrient import models

class Command(BaseCommand):
	def handle(self, *args, **options):
		#todo initialize a test setup or a good setup for testing
		pass
		# models.UnitOfMeasure(name)
		# models.Nutrient(name)
		# models.Standard(name)
		# models.Constraint(standard, nutrient, quantity, max_quantity)
		# models.Tag(name)
		# models.Product(name, tags, price)
