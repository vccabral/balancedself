

var mealAppAPI = angular.module(
	'mealApp.API',[
		'ngResource'
	]
);

mealAppAPI.constant('api_url', url_base+'/api/v1/');
mealAppAPI.constant('user', user);
mealAppAPI.constant('user_id', user_id);
mealAppAPI.constant('authenticated', authenticated);

mealAppAPI.factory('Standard', function(api_url, $resource) {
	return $resource(api_url+"standard/:id")
});

mealAppAPI.factory('Nutrient', function(api_url, $resource) {
	return $resource(api_url+"nutrient/:id")
});

mealAppAPI.factory('Product', function(api_url, $resource) {
	return $resource(api_url+"product/:id")
});

mealAppAPI.factory('Tag', function(api_url, $resource) {
	return $resource(api_url+"tag/:id")
});

mealAppAPI.factory('MealPlan', function(api_url, $resource) {
	return $resource(api_url+"mealplan/:id#")
});
