from nutrient.models import Standard, Nutrient, Product, Tag, Constraint, UnitOfMeasure
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from nutrient import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404
import sys
import numpy as np
from decimal import *
from pulp import LpProblem, LpVariable, LpMinimize, lpSum

class ConstraintViewSet(viewsets.ModelViewSet):
	queryset = Constraint.objects.all()
	serializer_class = serializers.ConstraintModelSerializer

class StandardViewSet(viewsets.ModelViewSet):
	queryset = Standard.objects.all()
	serializer_class = serializers.StandardHyperlinkedModelSerializer

class NutrientViewSet(viewsets.ModelViewSet):
	queryset = Nutrient.objects.all()
	serializer_class = serializers.NutrientHyperlinkedModelSerializer

class UnitOfMeasureViewSet(viewsets.ModelViewSet):
	queryset = UnitOfMeasure.objects.all()
	serializer_class = serializers.UnitOfMeasureModelSerializer

class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = serializers.ProductHyperlinkedModelSerializer

class TagViewSet(viewsets.ModelViewSet):
	queryset = Tag.objects.all()
	serializer_class = serializers.TagHyperlinkedModelSerializer


class MealPlan(object):

	def __init__(self, standard, must_haves, must_not_haves, nutrients, products, span):
		span_map = {
			"day": 1,
			"week": 7,
			"biweekly": 14,
			"monthly": int(365/12.0)
		}
		self.standard = standard
		self.must_haves = must_haves
		self.must_not_haves = must_not_haves
		self.nutrients = nutrients
		self.products = products
		self.days = span_map[span]

	def get_nutrient_min(self, nutrient):
		nutrient_key = str(nutrient.pk)
		if nutrient_key in self.nutrients and "low" in self.nutrients[nutrient_key] and self.nutrients[nutrient_key]["low"]:
			return -float(self.nutrients[nutrient_key]["low"])*self.days
		elif nutrient_key in self.nutrients and "low" in self.nutrients[nutrient_key] and not self.nutrients[nutrient_key]["low"]:
			return 0
		elif self.standard.constraints.filter(nutrient=nutrient).exists():
			nutrient_constraint = self.standard.constraints.filter(nutrient=nutrient)[0]
			if nutrient_constraint.quantity:
				return -nutrient_constraint.quantity*self.days
		return 0

	def get_nutrient_max(self, nutrient):
		nutrient_key = str(nutrient.pk)
		if nutrient_key in self.nutrients and "high" in self.nutrients[nutrient_key] and self.nutrients[nutrient_key]["high"]:
			return float(self.nutrients[nutrient_key]["high"])*self.days
		elif nutrient_key in self.nutrients and "high" in self.nutrients[nutrient_key] and not self.nutrients[nutrient_key]["high"]:
			return 1000000
		elif self.standard.constraints.filter(nutrient=nutrient).exists():
			nutrient_constraint = self.standard.constraints.filter(nutrient=nutrient)[0]
			if nutrient_constraint.max_quantity:
				return nutrient_constraint.max_quantity*self.days
		return 1000000

	def calculate_maximum_plan(self):
		result = {}
		result['standard'] = self.standard.id
		result['must_haves'] = self.must_haves
		result['must_not_haves'] = self.must_not_haves
		result['nutrients'] = self.nutrients
		result['products'] = self.products

		if result['must_haves']:
			product_list = Product.objects.filter(confirmed=True, tags__pk__in=self.must_haves).exclude(tags__pk__in=self.must_not_haves)
		else:
			product_list = Product.objects.filter(confirmed=True).exclude(tags__pk__in=self.must_not_haves)
		result['product_list'] = product_list.values_list('name', flat=True)

		if len(product_list) == 0:
			result['success'] = False
			return result

		constraints = self.standard.constraints.all()
		try:
			c = map(float, product_list.values_list('price', flat=True))
			b = np.zeros((Nutrient.objects.all().count()*2,))
			A = np.zeros((Nutrient.objects.all().count()*2, product_list.count()))

			print("initializing array b")
			for i, nutrient in enumerate(Nutrient.objects.all()):
				b[i*2] = self.get_nutrient_min(nutrient)
				b[i*2+1] = self.get_nutrient_max(nutrient)

			print("initializing matrix A")
			for i, nutrient in enumerate(Nutrient.objects.all()):
				for j, product in enumerate(product_list):
					nutrient_info = product.nutrition_facts.filter(nutrient=nutrient)
					if nutrient_info.exists():
						A[i*2][j] = -nutrient_info[0].quantity
						A[i*2+1][j] = nutrient_info[0].quantity
					else:
						A[i*2][j] = 0
						A[i*2+1][j] = 0
			# print(A)

			prob = LpProblem("myProblem", LpMinimize)

			x = [LpVariable(
					"x_"+str(x.name), 
					int(self.products[str(x.id)]["low"]) if self.products[str(x.id)]["low"] else 0,
					int(self.products[str(x.id)]["high"]) if self.products[str(x.id)]["high"] else None,
					cat='Integer'
				) for i,x in enumerate(product_list)]
			prob += lpSum([xp*cp for xp, cp in zip(x, c)]), "Total Cost of Ingredients per can" #[ for ]
			for row, cell in zip(A, b):
				prob += lpSum(ap*xp for ap, xp in zip(row,  x)) <= cell

			solved = prob.solve()
			# print(prob)
			if len(prob.variables()) != 0:
				result['success'] = prob.status == 1
				if result['success']:
					result['reason'] = "we found a match"
				else:
					result['reason'] = "problem is unsolvable: "+str(prob.status)
				result['product_line_items'] = [
					{
						'name': product,
						'id': Product.objects.get(name=product).id,
						'product_quantity': quantity.varValue,
						'product_package_size': Product.objects.get(name=product).quanity_needed,
						'price': cost,
						'nutrition_info': {
							nutrient_info.nutrient.id: {
								"quantity": quantity.varValue,
								"package_size": nutrient_info.quantity,
								"unit": nutrient_info.nutrient.unit.name
							}
							for nutrient_info in Product.objects.get(name=product).nutrition_facts.all()
						}
					} for product, quantity, cost in zip(result['product_list'], prob.variables(), c)
				]
				result['product_total'] = reduce(lambda x, y:x+y['price']*y['product_quantity'], result['product_line_items'], 0)
				result['nutrition_info_line_items'] = {}
				for nutrient in Nutrient.objects.all():
					total = 0 
					for product, x in zip(product_list, prob.variables()):
						if product.nutrition_facts.all().filter(nutrient=nutrient).exists():
							quantity = product.nutrition_facts.all().filter(nutrient=nutrient)[0].quantity
							total = total + float(quantity) * float(x.varValue)
					result['nutrition_info_line_items'][nutrient.pk] = {
						"name": nutrient.name,
						"total": total
					}
				result['cost'] = sum([cp*xp.varValue for cp, xp in zip(c, prob.variables())])
				return result
			else:
				result['success'] = False
				result['reason'] = "problem is unsolvable"
				return result
		except:
			result['success'] = False
			result['reason'] = "An error was thrown: "+str(sys.exc_info()[0])
			raise
			return result

class MealPlanAPIView(APIView):
	def get(self, request, *args, **kw):
		standard = get_object_or_404(Standard, pk=request.GET.get('mealplan', 0))
		must_haves = request.GET.getlist('must_haves', [])
		must_not_haves = request.GET.getlist('must_not_haves', [])
		span = request.GET.get("span", "day")
		nutrients = {
			str(nutrient.pk): {
				"low": request.GET.get("nutrient_"+str(nutrient.pk)+"_low", None),
				"high": request.GET.get("nutrient_"+str(nutrient.pk)+"_high", None),
				"name": nutrient.name
			} for nutrient in Nutrient.objects.all()
		}

		products = {
			str(product.pk): {
				"low": request.GET.get("product_"+str(product.pk)+"_low", None),
				"high": request.GET.get("product_"+str(product.pk)+"_high", None),
				"name": product.name
			} for product in Product.objects.all()
		}

		mealplan = MealPlan(standard, must_haves, must_not_haves, nutrients, products, span)
		result = mealplan.calculate_maximum_plan()
		response = Response(result, status=status.HTTP_200_OK)
		return response

