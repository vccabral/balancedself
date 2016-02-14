from nutrient.models import Standard, Constraint, Nutrient, UnitOfMeasure, Product, Tag, NutritionFact
from rest_framework import serializers


class UnitOfMeasureModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = UnitOfMeasure
		fields = ('name', 'id')

class NutrientModelSerializer(serializers.ModelSerializer):
	unit = UnitOfMeasureModelSerializer()
	class Meta:
		model = Nutrient
		fields = ('name', 'unit', 'id')

class ConstraintModelSerializer(serializers.ModelSerializer):
	nutrient = NutrientModelSerializer(read_only=True)
	class Meta:
		model = Constraint
		fields = ('quantity', 'max_quantity', 'nutrient', 'id')

class TagModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = ('name', 'id')

class NutrientInfoModelSerializer(serializers.ModelSerializer):
	nutrient_readonly = NutrientModelSerializer(source='nutrient', read_only=True)
	down_votes = serializers.SerializerMethodField()
	up_votes = serializers.SerializerMethodField()
	votes = serializers.SerializerMethodField()

	def get_up_votes(self, obj):
		return obj.corroborate.all().count()

	def get_down_votes(self, obj):
		return obj.dispute.all().count()

	def get_votes(self, obj):
		return obj.corroborate.all().count() - obj.dispute.all().count()

	class Meta:
		model = NutritionFact
		fields = ('quantity', 'id', 'nutrient', 'nutrient_readonly', 'down_votes', 'up_votes', 'votes', 'from_manufacturer', 'from_trusted_unpaid_thirdparty', 'company_verified', 'from_user')



class StandardHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
	constraints_readonly = ConstraintModelSerializer(many=True, source='constraints', read_only=True)
	class Meta:
		model = Standard
		fields = ('url', 'name', 'constraints_readonly', 'id')

class NutrientHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
	unit_readonly = UnitOfMeasureModelSerializer(source='unit')
	class Meta:
		model = Nutrient
		fields = ('url', 'name', 'unit', 'unit_readonly', 'minimum_scale', 'maximum_scale', 'number_of_ticks', 'id')


class ProductHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
	tags = TagModelSerializer(many=True)
	class Meta:
		model = Product
		fields = ('url', 'quanity_as_listed', 'tags', 'price', 'name', 'id', 'quanity_needed', 'quantity', 'max_quantity', 'custom_span')


class TagHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Tag
		fields = ('url', 'name', 'id')



