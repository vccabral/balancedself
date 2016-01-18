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

	def get_nutrient_min(self, nutrient, span):
		listed_quantity = float(self.request.GET.get("nutrient_"+str(nutrient.pk)+"_low", 0))
		return - listed_quantity * span

	def get_nutrient_max(self, nutrient, span):
		listed_quantity = self.request.GET.get("nutrient_"+str(nutrient.pk)+"_high", None)
		return float(listed_quantity) * span if listed_quantity else None

	def get_product_min(self, product, span):
		listed_quantity = self.request.GET.get("product_"+str(product.pk)+"_low", None)
		return float(listed_quantity) * span / 7.0 if listed_quantity else 0

	def get_product_max(self, product, span):
		listed_quantity = self.request.GET.get("product_"+str(product.pk)+"_high", None)
		return float(listed_quantity) * span if listed_quantity else None

	def calculate_maximum_plan(self):
		result = {}
		must_haves = self.request.GET.getlist('must_haves', [])
		must_not_haves = self.request.GET.getlist('must_not_haves', [])
		span = int(self.request.GET.get("span", 7))

		if must_haves:
			product_list = Product.objects.filter(confirmed=True, tags__pk__in=must_haves).exclude(tags__pk__in=must_not_haves)
		else:
			product_list = Product.objects.filter(confirmed=True).exclude(tags__pk__in=must_not_haves)

		products = list(product_list)
		nutrients = list(Nutrient.objects.all())

		if len(product_list) == 0:
			result['success'] = False

		else:
			try:
				max_count = sum(1 if self.get_nutrient_max(nutrient, span) else 0 for nutrient in nutrients)

				print("initializing c")
				c = map(float, map(lambda product: product.price, products))
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

					for j, product in enumerate(products):
						A[i][j] = - product.nutrition_facts.filter(nutrient=nutrient)[0].quantity
					i = i + 1

					if tmp:
						for j, product in enumerate(products):
							A[i][j] = product.nutrition_facts.filter(nutrient=nutrient)[0].quantity
						i = i + 1
				print(A)


				prob = LpProblem("myProblem", LpMinimize)

				print("filling matrix x")
				x = [LpVariable(
						"x_"+str(product.name), 
						self.get_product_min(product, span),
						self.get_product_max(product, span),
						cat='Integer'
					) for product in products]
				print(x)


				print("initializing matrix cost")
				prob += lpSum([xp*cp for xp, cp in zip(x, c)]), "Total Cost of Ingredients per can" #[ for ]
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
							'name': product.name,
							'id': product.id,
							'product_quantity': quantity.varValue,
							'product_package_size': product.quanity_needed,
							'price': cost,
							'nutrient_totals': {
								nutrient.id: float(quantity.varValue) * float(product.nutrition_facts.filter(nutrient=nutrient)[0].quantity)
								for nutrient in nutrients
							}
						} for product, quantity, cost in zip(products, prob.variables(), c)
					]
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
