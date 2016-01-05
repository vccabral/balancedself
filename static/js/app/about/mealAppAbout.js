var mealAppAbout = angular.module(
	'mealApp.About', [
		'ngRoute'
	]
);


mealAppAbout.config(function($routeProvider, $locationProvider){
    $routeProvider
    .when('/about', {
        templateUrl: 'static/js/app/about/about.html'
    })
});