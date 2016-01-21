from nutrient.models import Standard, Nutrient, Product, Tag, Constraint, UnitOfMeasure
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
import sys
import numpy as np
import django_filters

from nutrient import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404
from decimal import *
from pulp import LpProblem, LpVariable, LpMinimize, lpSum
from rest_framework import filters
from rest_framework import generics
from django.forms.models import model_to_dict


class StandardFilter(django_filters.FilterSet):
    class Meta:
        model = Standard
        fields = ['name']

class StandardViewSet(viewsets.ModelViewSet):
	queryset = Standard.objects.all()
	serializer_class = serializers.StandardHyperlinkedModelSerializer
	filter_class = StandardFilter

	def get_queryset(self):
		return Standard.objects.all().prefetch_related("constraints__nutrient__unit")



class NutrientFilter(django_filters.FilterSet):
    class Meta:
        model = Nutrient
        fields = ['name']

class NutrientViewSet(viewsets.ModelViewSet):
	queryset = Nutrient.objects.all()
	serializer_class = serializers.NutrientHyperlinkedModelSerializer
	filter_class = NutrientFilter

	def get_queryset(self):
		return Nutrient.objects.all().select_related("unit")


class UnitOfMeasureFilter(django_filters.FilterSet):
    class Meta:
        model = UnitOfMeasure
        fields = ['name']

class UnitOfMeasureViewSet(viewsets.ModelViewSet):
	queryset = UnitOfMeasure.objects.all()
	serializer_class = serializers.UnitOfMeasureModelSerializer
	filter_class = UnitOfMeasureFilter



class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['name']

class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = serializers.ProductHyperlinkedModelSerializer
	filter_class = ProductFilter
	
	def get_queryset(self):
		return Product.objects.all().prefetch_related("nutrition_facts", "tags")



class TagFilter(django_filters.FilterSet):
    class Meta:
        model = Tag
        fields = ['name']

class TagViewSet(viewsets.ModelViewSet):
	queryset = Tag.objects.all()
	serializer_class = serializers.TagHyperlinkedModelSerializer
	filter_class = TagFilter


class CustomMealPlan(object):

	def __init__(self, request):
		self.request = request

	def get_listed_quantity(self, key_name, default_val):
		if key_name in self.request.DATA:
			return self.request.DATA[key_name]
		elif key_name in self.request.POST:
			return self.request.POST[key_name]
		else:
			return self.request.GET.get(key_name, default_val)

	def get_nutrient_min(self, nutrient, span):
		listed_quantity = float(self.get_listed_quantity("nutrient_"+str(nutrient.pk)+"_low", 0))
		return - listed_quantity * span

	def get_nutrient_max(self, nutrient, span):
		listed_quantity = self.get_listed_quantity("nutrient_"+str(nutrient.pk)+"_high", None)
		return float(listed_quantity) * span if listed_quantity else None

	def get_product_min(self, product, span):
		listed_quantity = self.get_listed_quantity("product_"+str(product['id'])+"_low", None)
		return float(listed_quantity) * span / 7.0 if listed_quantity else 0

	def get_product_max(self, product, span):
		listed_quantity = self.get_listed_quantity("product_"+str(product['id'])+"_high", None)
		return float(listed_quantity) * span if listed_quantity else None

	def calculate_maximum_plan(self):
		result = {}
		span = int(self.get_listed_quantity("span", 7))

		product_list = Product.objects.filter(confirmed=True)
		products_queryset = product_list.prefetch_related("nutrition_facts__nutrient")

		products = [
			(
				model_to_dict(product), 
				{
					nutrient_fact.nutrient.id: nutrient_fact.quantity
					for nutrient_fact in product.nutrition_facts.all()
				}
			) for product in products_queryset
		]

		nutrients = list(Nutrient.objects.all())

		if len(product_list) == 0:
			result['success'] = False

		else:
			try:
				max_count = sum(1 if self.get_nutrient_max(nutrient, span) else 0 for nutrient in nutrients)

				print("initializing c")
				c = map(float, map(lambda product: product[0]['price'], products))
				print("initializing b")
				b = np.zeros((len(nutrients)+max_count,))
				print("initializing A")
				A = np.zeros((len(nutrients)+max_count, len(products)))

				print("filling array b")
				i = 0 
				for nutrient in nutrients:
					b[i] = self.get_nutrient_min(nutrient, span)
					i = i + 1
					tmp = self.get_nutrient_max(nutrient, span)
					if tmp:
						b[i] = tmp
						i = i + 1
				print(b)

				print("filling matrix A")
				i = 0
				for nutrient in nutrients:
					tmp = self.get_nutrient_max(nutrient, span)

					for j, (product, nutrient_facts_dict) in enumerate(products):
						A[i][j] = - nutrient_facts_dict[nutrient.id]
					i = i + 1

					if tmp:
						for j, (product, nutrient_facts_dict) in enumerate(products):
							A[i][j] = nutrient_facts_dict[nutrient.id]
						i = i + 1
				print(A)


				prob = LpProblem("myProblem", LpMinimize)

				print("filling matrix x")
				x = [LpVariable(
						"x_"+str(product['name']), 
						self.get_product_min(product, span),
						self.get_product_max(product, span),
						cat='Integer'
					) for (product, fact) in products]
				print(x)


				print("initializing matrix cost")
				prob += lpSum([xp*cp for xp, cp in zip(x, c)]), "Total Cost of Ingredients per can" 
				for row, cell in zip(A, b):
					prob += lpSum(ap*xp for ap, xp in zip(row,  x)) <= cell
				print(prob)

				solved = prob.solve()


				if len(prob.variables()) != 0:
					result['success'] = prob.status == 1
					if result['success']:
						result['reason'] = "we found a match"
					else:
						result['reason'] = "problem is unsolvable: "+str(prob.status)
					result['product_line_items'] = [
						{
							'name': product['name'],
							'id': product['id'],
							'product_quantity': quantity.varValue,
							'product_package_size': product['quanity_needed'],
							'price': cost,
							'nutrient_totals': {
								nutrient.id: float(quantity.varValue) * float(nutrient_facts_dict[nutrient.id])
								for nutrient in nutrients
							}
						} for (product, nutrient_facts_dict), quantity, cost in zip(products, prob.variables(), c)
					]
					result['nutrition_info_line_items'] = {}
					for nutrient in nutrients:
						total = 0 
						for (product, nutrient_facts_dict), x in zip(products, prob.variables()):
							quantity = nutrient_facts_dict[nutrient.id]
							total = total + float(quantity) * float(x.varValue)
						result['nutrition_info_line_items'][nutrient.pk] = {
							"name": nutrient.name,
							"total": total
						}

					result['cost'] = sum([cp*xp.varValue for cp, xp in zip(c, prob.variables())])
					result['product_total'] = reduce(lambda x, y:x+y['price']*y['product_quantity'], result['product_line_items'], 0)
					return result
				else:
					result['success'] = False
					result['reason'] = "problem is unsolvable"
					result['nutrition_info_line_items'] = {}
					for nutrient in nutrients:
						total = 0 
						for product, x in zip(products, prob.variables()):
							if product.nutrition_facts.all().filter(nutrient=nutrient).exists():
								quantity = product.nutrition_facts.all().filter(nutrient=nutrient)[0].quantity
								total = total + float(quantity) * float(x.varValue)
						result['nutrition_info_line_items'][nutrient.pk] = {
							"name": nutrient.name,
							"total": total
						}

					result['cost'] = sum([cp*xp.varValue for cp, xp in zip(c, prob.variables())])
					result['product_total'] = reduce(lambda x, y:x+y['price']*y['product_quantity'], result['product_line_items'], 0)

				return result
			except:
				result['success'] = False
				result['reason'] = "An error was thrown: "+str(sys.exc_info()[0])
				raise
				return result
		return result


class CustomMealPlanAPIView(APIView):

	def get(self, request, *args, **kw):
		mealplan = CustomMealPlan(request)
		result = mealplan.calculate_maximum_plan()
		response = Response(result, status=status.HTTP_200_OK)
		return response

	def post(self, request, *args, **kw):
		mealplan = CustomMealPlan(request)
		result = mealplan.calculate_maximum_plan()
		response = Response(result, status=status.HTTP_200_OK)
		return response
