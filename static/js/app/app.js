
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

mealApp.config(function($routeProvider, $locationProvider){
    $routeProvider
    .otherwise({
        redirectTo: '/mealplans'
    });
});