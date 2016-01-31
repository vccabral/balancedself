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
		ordering = ['importance','name', 'pk']

	def __str__(self):

		from nutrient.models import Product
		products = Product.objects.filter(nutrition_facts__nutrient=self, nutrition_facts__quantity__gt=0).count()
		return str(self.name)+"("+self.unit.name+") "+str(products)+" products "

class Standard(models.Model):
	name = models.CharField(max_length=200, unique=True)
	user = models.ForeignKey(User, null=True, blank=True)

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
	quantity = models.IntegerField(default=0)
	max_quantity = models.IntegerField(default=7)

	class Meta:
		ordering = ['name']

	def get_complete(self):
		all_nutrients = all(map(lambda x: self.nutrition_facts.all().filter(nutrient__name=x.name), Nutrient.objects.all()))
		duplicate_nutrients = any(map(lambda x: self.nutrition_facts.all().filter(nutrient__name=x.name).count()>1, Nutrient.objects.all()))
		has_quanity_needed = self.quanity_needed
		return all_nutrients and not duplicate_nutrients and has_quanity_needed

	def page_to_array_of_nutrient_info(self):
		import urllib2
		import re
		import demjson
		from bs4 import BeautifulSoup

		nutrients = ["Calories","Fat","Carbohyrates","Fiber","Sugars","Protein","Vitamin A","Vitamin C","Vitamin D","Vitamin E","Vitamin K","Thiamin","Riboflavin","Niacin","Vitamin B6","Folate","Vitamin B12","Pantothenic Acid","Choline","Betaine","Calcium","Iron","Magnesium","Phosphorus","Potassium","Sodium","Zinc","Copper","Manganese","Selenium","Cholesterol"]
		nutrients_id = [0,14,4,5,7,77,97,100,101,102,103,107,108,109,110,111,115,116,143,144,117,118,119,120,121,122,123,124,125,126,72]
		response = urllib2.urlopen(self.url)
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


	def save(self, *args, **kwargs):
		is_create = not self.pk
		super(Product, self).save(*args, **kwargs) 
		if is_create and self.url:

			nutrient_info, product_unit, raw_joson = self.page_to_array_of_nutrient_info()
			nutrients = ["Calories","Fat","Carbohyrates","Fiber","Sugars","Protein","Vitamin A","Vitamin C","Vitamin D","Vitamin E","Vitamin K","Thiamin","Riboflavin","Niacin","Vitamin B6","Folate","Vitamin B12","Pantothenic Acid","Choline","Betaine","Calcium","Iron","Magnesium","Phosphorus","Potassium","Sodium","Zinc","Copper","Manganese","Selenium","Cholesterol"]
			self.raw_data_body = raw_joson
			self.save()

			needed_quantity = float(self.quanity_as_listed) / 100.0

			for nutrient, quantity in zip(nutrients, nutrient_info):
				NutritionFact.objects.create(
					product = self, 
					nutrient_id = Nutrient.objects.get(name=nutrient).id,
					quantity = quantity * needed_quantity
				)

	def __str__(self):
		return self.name

class NutritionFact(models.Model):
	product = models.ForeignKey(Product, related_name='nutrition_facts')
	nutrient = models.ForeignKey(Nutrient)
	quantity = models.DecimalField(decimal_places=3, max_digits=12)
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
