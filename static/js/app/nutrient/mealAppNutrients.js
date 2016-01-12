var mealAppNutrients = angular.module(
	'mealApp.Nutrients', [
		'mealApp.API',
		'ngRoute'
	]
);


mealAppNutrients.controller('NutrientController', function($scope, Nutrient){
	$scope.page_info = {
		'nutrients': Nutrient.get() 
	};

});

mealAppNutrients.config(function($routeProvider, $locationProvider){
    $routeProvider
    .when('/nutrients', {
        templateUrl: 'static/js/app/nutrient/nutrient.html',
        controller: 'NutrientController'
    })
});