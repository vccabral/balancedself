var mealAppStandards = angular.module(
	'mealApp.Standards', [
		'mealApp.API',
		'ngRoute'
	]
);


mealAppStandards.controller('StandardController', function($scope, Standard){
	$scope.page_info = {};

});

mealAppStandards.config(function($routeProvider, $locationProvider){
    $routeProvider
    .when('/standards', {
        templateUrl: 'static/js/app/standard/standard.html',
        controller: 'StandardController'
    })
});