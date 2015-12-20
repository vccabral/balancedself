from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers
from nutrient import views
from nutrient import models
from django.utils.functional import curry
from django.views.generic.base import RedirectView


models_list = [models.RawData,models.UnitOfMeasure,models.Nutrient,models.Standard,models.Constraint,models.Tag,models.Product,models.NutritionFact]
for model in models_list:
	try:
		if model not in [models.Product, models.Standard]:
			admin.site.register(model)
	except:
		pass

class NutritionFactInline(admin.TabularInline):
	model = models.NutritionFact
	def get_extra(self, request, obj=None, **kwargs):
		if obj:
			return models.Nutrient.objects.all().count() - obj.nutrition_facts.all().count()	
		return models.Nutrient.objects.all().count()
	def get_formset(self, request, obj=None, **kwargs):
		initial = []
		if request.method == "GET":
			for nutrient in models.Nutrient.objects.all():
				initial.append({
					'quantity': 0,
					'nutrient': nutrient
				})
		formset = super(NutritionFactInline, self).get_formset(request, obj, **kwargs)
		formset.__init__ = curry(formset.__init__, initial=initial)
		return formset

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
	inlines = [NutritionFactInline]

class ConstraintInline(admin.TabularInline):
	model = models.Constraint
	def get_extra(self, request, obj=None, **kwargs):
		if obj:
			return models.Nutrient.objects.all().count() - obj.constraints.all().count()	
		return models.Nutrient.objects.all().count()
	def get_formset(self, request, obj=None, **kwargs):
		initial = []
		if request.method == "GET":
			for nutrient in models.Nutrient.objects.all():
				initial.append({
					'quantity': 0,
					'nutrient': nutrient
				})
		formset = super(ConstraintInline, self).get_formset(request, obj, **kwargs)
		formset.__init__ = curry(formset.__init__, initial=initial)
		return formset


@admin.register(models.Standard)
class StandardAdmin(admin.ModelAdmin):
	inlines = [ConstraintInline]

class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

router = routers.DefaultRouter()
router.register(r'constraint', views.ConstraintViewSet)
router.register(r'unitofmeasure', views.UnitOfMeasureViewSet)
router.register(r'standard', views.StandardViewSet)
router.register(r'nutrient', views.NutrientViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'tag', views.TagViewSet)


urlpatterns = [
	url('', include('social.apps.django_app.urls', namespace='social')),
	url(r'^$', HomePageView.as_view(), name='home'),
	url(r'^accounts/profile/$', RedirectView.as_view(url='/'), name='before_home'),
	url(r'^api/v1/', include(router.urls)),
	url(r'^api/v1/mealplan/$', views.MealPlanAPIView.as_view(), name='mealplan'),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^admin/', include(admin.site.urls)),
]
