from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers
from nutrient import views
from nutrient import models
from django.utils.functional import curry
from django.views.generic.base import RedirectView


models_list = [
	models.RawData,
	models.UnitOfMeasure,
	models.Nutrient,
	models.Standard,
	models.Constraint,
	models.Tag,
	models.Product,
	models.NutritionFact
]
for model in models_list:
	try:
		admin.site.register(model)
	except:
		pass
		

class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

router = routers.DefaultRouter()
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
	url(r'^api/v1/mealplan/$', views.CustomMealPlanAPIView.as_view(), name='mealplan'),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^admin/', include(admin.site.urls)),
]
