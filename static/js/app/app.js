
var mealApp = angular.module(
	'mealApp', [
		'ngRoute',
		'mealApp.About',
		'mealApp.Products',
		'mealApp.Nutrients',
		'mealApp.Standards',
		'mealApp.MealPlans'
	]
);

mealApp.config(function($routeProvider, $locationProvider, $httpProvider){
    $routeProvider
    .otherwise({
        redirectTo: '/mealplans'
    });

	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});