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
		return float(listed_quantity) * span if listed_quantity else 0

	def get_product_max(self, product, span):
		listed_quantity = self.get_listed_quantity("product_"+str(product['id'])+"_high", None)
		return float(listed_quantity) * span if listed_quantity is not None else None

	def get_product_list(self):
		product_list = Product.objects.filter(confirmed=True)
		products_queryset = product_list.prefetch_related("nutrition_facts__nutrient").order_by("id")

		products = [
			(
				model_to_dict(product), 
				{
					nutrient_fact.nutrient.id: nutrient_fact.quantity
					for nutrient_fact in product.nutrition_facts.all()
				}
			) for product in products_queryset
		]
		return products

	def get_nutrients(self):
		return list(Nutrient.objects.all())

	def create_c(self, products):
		return map(float, map(lambda product: product[0]['price'], products))

	def create_b(self, nutrients, number_of_maximums_provided, span):
		b = np.zeros((len(nutrients)+number_of_maximums_provided,))
		i = 0 
		for nutrient in nutrients:
			b[i] = self.get_nutrient_min(nutrient, span)
			i = i + 1
			tmp = self.get_nutrient_max(nutrient, span)
			if tmp:
				b[i] = tmp
				i = i + 1
		return b

	def create_A(self, nutrients, products, number_of_maximums_provided, span):
		A = np.zeros((len(nutrients)+number_of_maximums_provided, len(products)))
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

		return A

	def get_x_name_from_product(self, product):
		return "x_"+str(product['name']).replace (" ", "_")

	def create_x(self, products, span):
		return [LpVariable(
			self.get_x_name_from_product(product), 
			self.get_product_min(product, span),
			self.get_product_max(product, span),
			cat='Integer'
			) for (product, fact) in products]

	def get_linear_program_solution(self, c, b, A, x):
		prob = LpProblem("myProblem", LpMinimize)
		prob += lpSum([xp*cp for xp, cp in zip(x, c)]), "Total Cost of Ingredients per can" 

		for row, cell in zip(A, b):
			prob += lpSum(ap*xp for ap, xp in zip(row,  x)) <= cell

		solved = prob.solve()
		return prob


	def calculate_maximum_plan(self):
		result = {}
		span = int(self.get_listed_quantity("span", 7))
		products = self.get_product_list()
		nutrients = self.get_nutrients()

		if len(products) == 0:
			result['success'] = False
		else:
			try:
				number_of_maximums_provided = sum(1 if self.get_nutrient_max(nutrient, span) else 0 for nutrient in nutrients)

				c = self.create_c(products)
				b = self.create_b(nutrients, number_of_maximums_provided, span)
				A = self.create_A(nutrients, products, number_of_maximums_provided, span)
				x = self.create_x(products, span)

				prob = self.get_linear_program_solution(c, b, A, x)

				solution_variables = []
				for product, nutrient_facts_dict in products:
					x_name = self.get_x_name_from_product(product)
					for x_var in prob.variables():
						if str(x_var) == x_name:
							solution_variables.append(x_var)
							break
					else:
						print("no one found for: ", x_name)

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
						} for (product, nutrient_facts_dict), quantity, cost in zip(products, solution_variables, c)
					]
					result['nutrition_info_line_items'] = {}
					for nutrient in nutrients:
						total = 0 
						for (product, nutrient_facts_dict), x in zip(products, solution_variables):
							quantity = nutrient_facts_dict[nutrient.id]

							total = total + float(quantity) * float(x.varValue)
						result['nutrition_info_line_items'][nutrient.id] = {
							"name": nutrient.name,
							"total": total
						}

					result['cost'] = sum([cp*xp.varValue for cp, xp in zip(c, solution_variables)])
					result['product_total'] = reduce(lambda x, y:x+y['price']*y['product_quantity'], result['product_line_items'], 0)
					return result
				else:
					result['success'] = False
					result['reason'] = "problem is unsolvable"
					result['nutrition_info_line_items'] = {}
					for nutrient in nutrients:
						total = 0 
						for product, x in zip(products, solution_variables):
							quantity = nutrient_facts_dict[nutrient.id]
							total = total + float(quantity) * float(x.varValue)
						result['nutrition_info_line_items'][nutrient.pk] = {
							"name": nutrient.name,
							"total": total
						}

					result['cost'] = sum([cp*xp.varValue for cp, xp in zip(c, solution_variables)])
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
