from django.db import models
from django.utils.encoding import smart_str
from django.contrib.auth.models import User

class RawData(models.Model):
	name = models.CharField(max_length=200)
	unit = models.CharField(max_length=200)
	nutrient = models.CharField(max_length=200)
	product = models.CharField(max_length=200)

	def __str__(self):
		return self.product + " has " + self.name + self.unit + " of "+self.nutrient

	class Meta:
		ordering = ['product', 'nutrient']


class UnitOfMeasure(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return smart_str(self.name)

class Nutrient(models.Model):
	name = models.CharField(max_length=200, unique=True)
	unit = models.ForeignKey(UnitOfMeasure)
	minimum_scale = models.DecimalField(decimal_places=3, max_digits=9, blank=True, null=True)
	maximum_scale = models.DecimalField(decimal_places=3, max_digits=9, blank=True, null=True)
	number_of_ticks = models.IntegerField(blank=True, null=True)
	importance = models.IntegerField(default=1)

	class Meta:
		ordering = ['importance','name']

	def __str__(self):
		return str(self.name)+"("+self.unit.name+")"

class Standard(models.Model):
	name = models.CharField(max_length=200, unique=True)

	def __str__(self):
		return self.name	

class Constraint(models.Model):
	standard = models.ForeignKey(Standard, related_name='constraints')
	nutrient = models.ForeignKey(Nutrient)
	quantity = models.DecimalField(decimal_places=3, max_digits=9, blank=True, null=True)
	max_quantity = models.DecimalField(decimal_places=3, max_digits=9, blank=True, null=True)

	def __str__(self):
		label = str(self.nutrient.unit) + " of "+str(self.nutrient)
		more_than = " more than "+str(self.quantity) + label if self.quantity else ""
		less_than = " less than "+str(self.max_quantity) if self.max_quantity else ""
		return str(self.standard) + " standard says take "+more_than+less_than

	class Meta:
		ordering = ['nutrient']
		unique_together = (("standard", "nutrient"),)

class Tag(models.Model):
	name = models.CharField(max_length=200, unique=True)	

	def __str__(self):
		return self.name	

class Product(models.Model):
	name = models.CharField(max_length=200, unique=True)
	tags = models.ManyToManyField(Tag, blank=True)
	price = models.DecimalField(decimal_places=2, max_digits=6)
	confirmed = models.BooleanField(default=False)
	url = models.URLField(blank=True, default="")
	quanity_as_listed = models.CharField(max_length=200, blank=True, default="")
	quanity_needed = models.CharField(max_length=200, blank=True, default="")
	raw_data_body = models.CharField(max_length=10000, blank=True, default="")
	conversion_factor = models.DecimalField(decimal_places=5, max_digits=12, default=0)
	has_been_converted = models.BooleanField(default=False)

	class Meta:
		ordering = ['name']

	def get_complete(self):
		all_nutrients = all(map(lambda x: self.nutrition_facts.all().filter(nutrient__name=x.name), Nutrient.objects.all()))
		duplicate_nutrients = any(map(lambda x: self.nutrition_facts.all().filter(nutrient__name=x.name).count()>1, Nutrient.objects.all()))
		has_quanity_needed = self.quanity_needed
		return all_nutrients and not duplicate_nutrients and has_quanity_needed

	def __str__(self):
		if self.get_complete():
			return self.name+", flagged as complete"
		else:
			list_of_complete = []
			sublist_of_nutrients = self.nutrition_facts.all().values_list('nutrient', flat=True)
			total_nutrient_ids = Nutrient.objects.all().exclude(id__in=sublist_of_nutrients).values_list('name', flat=True)
			duplicate_nutrient = []
			for nutrient in sublist_of_nutrients:
				if self.nutrition_facts.all().filter(nutrient__pk=nutrient).count() > 1 and Nutrient.objects.get(pk=nutrient) not in duplicate_nutrient:
					duplicate_nutrient.append(Nutrient.objects.get(pk=nutrient))

			if len(duplicate_nutrient) > 0:
				return self.name + ", flagged as incomplete duplicate "+str(map(lambda x: x.name, duplicate_nutrient))+" nutrient(s)"
			if len(total_nutrient_ids) > 5:
				return self.name + ", flagged as incomplete on "+str(len(total_nutrient_ids))+"/"+str(Nutrient.objects.all().count())+" nutrient(s)"
			else:
				return self.name + ", flagged as incomplete on "+str(map(str, total_nutrient_ids))

class NutritionFact(models.Model):
	product = models.ForeignKey(Product, related_name='nutrition_facts')
	nutrient = models.ForeignKey(Nutrient)
	quantity = models.DecimalField(decimal_places=3, max_digits=9)
	corroborate = models.ManyToManyField(User, blank=True, related_name="corroborating_users")
	dispute = models.ManyToManyField(User, blank=True, related_name="disputing_users")
	from_manufacturer = models.BooleanField(default=False)
	from_trusted_unpaid_thirdparty = models.BooleanField(default=False)
	company_verified = models.BooleanField(default=False)
	from_user = models.BooleanField(default=True)

	class Meta:
		ordering = ['product__name']
		unique_together = (("product", "nutrient"),)

	def __str__(self):
		return smart_str(str(self.product.name) + " has " + str(self.quantity) + self.nutrient.unit.name + " " + str(self.nutrient))
