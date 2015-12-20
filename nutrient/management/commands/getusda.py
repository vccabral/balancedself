from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
from nutrient.models import RawData
import urllib2
import re

class Command(BaseCommand):
	def handle(self, *args, **options):
		base_url = "http://ndb.nal.usda.gov/ndb/foods/show/%s?fg=&man=&lfacet=&count=&max=35&qlookup=&offset=8610&sort=&format=Full&reportfmt=other&rptfrm=&ndbno=&nutrient1=&nutrient2=&nutrient3=&subset=&totCount=&measureby=&_action_show=Apply+Changes&Qv=1&Q1=1&Q2=1&Q3=1&Q4=1"
		max_iter = 7512
		macronutrients_dict = {}
		RawData.objects.all().delete()
		for foodid in range(1,max_iter+1):
			print(foodid*100.0/max_iter)
			url = base_url % foodid
			try:
				response = urllib2.urlopen(url)
				html_doc = response.read()
				soup = BeautifulSoup(html_doc)
				product_div = soup.find(id="view-name")
				product_name_arr = re.split('\d\d\d\d\d', product_div.get_text().strip())
				product_name = product_name_arr[-1][2:]
				trs = soup.find_all("tr")
				macronutrients = ["Water","Energy","Protein","Total lipid (fat)","Ash","Carbohydrate, by difference","Fiber, total dietary","Sugars, total","Calcium, Ca","Iron, Fe","Magnesium, Mg","Phosphorus, P","Potassium, K","Sodium, Na","Zinc, Zn","Copper, Cu","Manganese, Mn","Selenium, Se","Fluoride, F","Vitamin C, total ascorbic acid","Thiamin","Riboflavin","Niacin","Pantothenic acid","Vitamin B-6","Folate, total","Folic acid","Folate, food","Folate, DFE","Choline, total","Betaine","Vitamin B-12","Vitamin B-12, added","Vitamin A, RAE","Retinol","Carotene, beta","Carotene, alpha","Cryptoxanthin, beta","Vitamin A, IU","Lycopene","Lutein + zeaxanthin","Vitamin E (alpha-tocopherol)","Vitamin E, added","Tocopherol, beta","Tocopherol, gamma","Tocopherol, delta","Vitamin D (D2 + D3)","Vitamin D3 (cholecalciferol)","Vitamin D","Vitamin K (phylloquinone)","Fatty acids, total saturated","Fatty acids, total monounsaturated","Fatty acids, total polyunsaturated","Fatty acids, total trans","Fatty acids, total trans-monoenoic","Other","Alcohol, ethyl","Caffeine","Theobromine"]
				for tr in trs:
					tds = tr.find_all("td")
					if len(tds) == 9:
						name = tds[0].get_text().strip()
						name_parts = re.split(r'\s+\d+\s*', name)
						name = name_parts[0]
						if name in macronutrients:
							if not RawData.objects.filter(product=product_name, name=tds[2].get_text(), nutrient=name).exists():
								RawData.objects.create(
									name=tds[2].get_text(),
									unit=tds[1].get_text(),
									nutrient=name,
									product=product_name
								)
			except:
				pass
