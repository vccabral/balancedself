var mealAppProducts = angular.module(
	'mealApp.Products', [
		'mealApp.API',
		'ngRoute'
	]
);


mealAppProducts.controller('ProductsController', function($scope, Product){
	$scope.page_info = {
		'products': Product.get(),
		'message': "Our Food List"
	};

});

mealAppProducts.config(function($routeProvider, $locationProvider){
    $routeProvider
    .when('/products', {
        templateUrl: 'static/js/app/product/product.html',
        controller: 'ProductsController'
    })
});