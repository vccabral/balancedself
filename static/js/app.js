var mealApp = angular.module('mealApp', ['ngResource', 'ngRoute']);

mealApp.constant('api_url', '/api/v1/');
mealApp.constant('user', user);
mealApp.constant('user_id', user_id);
mealApp.constant('authenticated', authenticated);

mealApp.factory('Standard', function(api_url, $resource) {
	return $resource(api_url+"standard/:id")
});

mealApp.factory('Nutrient', function(api_url, $resource) {
	return $resource(api_url+"nutrient/:id")
});

mealApp.factory('Product', function(api_url, $resource) {
	return $resource(api_url+"product/:id")
});

mealApp.factory('Tag', function(api_url, $resource) {
	return $resource(api_url+"tag/:id")
});

mealApp.factory('MealPlan', function(api_url, $resource) {
	return $resource(api_url+"mealplan/:id")
});

mealApp.controller('MealPlannerController', function($scope, Standard, Tag, MealPlan, $timeout, $interval) {
	var findOptimalMealPlanClicks = 0;
	var findOptimalMealPlanLastClicks = 0;
	$interval(5000, function(){
		if(findOptimalMealPlanClicks!=0){
			if(findOptimalMealPlanLastClicks == findOptimalMealPlanClicks){
				findOptimalMealPlanClicks = 0;
				findOptimalMealPlanLastClicks = 0;
			}
		}
	});
	$scope.findOptimalMealPlanBrains = function(){
		var params = {
			'mealplan': $scope.page_info.selected_standard,
			'must_haves': $scope.page_info.must_haves,
			'must_not_haves': $scope.page_info.must_not_haves,
			'span': $scope.page_info.selected_span
		};
		for(var i=0;i<$scope.page_info.standard_constraints.length;i++){
			var d = $scope.page_info.standard_constraints[i];
			params['nutrient_'+d.nutrient.id+'_low'] = d.quantity;
			params['nutrient_'+d.nutrient.id+'_high'] = d.max_quantity;
		}
		$scope.page_info.mealplan = MealPlan.get(params);
	};
	$scope.findOptimalMealPlan = function(){
		findOptimalMealPlanClicks = findOptimalMealPlanClicks + 1;
		$timeout(function(){
			findOptimalMealPlanClicks = findOptimalMealPlanClicks - 1;
			if(findOptimalMealPlanClicks==0){
				$scope.findOptimalMealPlanBrains();
			}
		}, 1000);
	}
	var setMeal = function(index){
		$scope.page_info.selected_standard_name = $scope.page_info.standards.results[index].name;
		$scope.page_info.standard_constraints = angular.copy($scope.page_info.standards.results[index].constraints_readonly);
		$scope.findOptimalMealPlan();
	};
	$scope.page_info = {
		'message': 'Design your Diet',
		'standards': Standard.get(),
		'tags': Tag.get(),
		'selected_standard': 0,
		'must_haves': [],
		'must_not_haves': [],
		'selected_standard_name': '',
		'must_haves_name': [],
		'must_not_haves_name': [],
		'mealplan': false,
		'standard_constraints': [],
		'selected_span': 'week',
		'show_all_food': true,
		'selection_options': [{ "value": 'day', "text": "Daily" }, { "value": 'week', "text": "Weekly" }]
	};
	$scope.$watch(function(scope){
			return scope.page_info.selected_standard
		},
		function(newValue, oldValue){
			if(newValue!=0){
				var index = 0;
				while($scope.page_info.standards.results[index].id != newValue){
					index = index + 1;
				}
				setMeal(index);
			}
		}
	);

	$scope.$watch(function(scope){
			return scope.page_info.must_haves
		},
		function(newValue, oldValue){
			var new_must_haves = [];
			for(var indexOfValue = 0;indexOfValue<newValue.length;indexOfValue++){
				var tag_index = 0;
				while($scope.page_info.tags.results[tag_index].id != newValue[indexOfValue]){
					tag_index = tag_index + 1;
				}
				new_must_haves.push($scope.page_info.tags.results[tag_index].name);
			}
			$scope.page_info.must_haves_name = new_must_haves;
		}
	);

	$scope.$watch(function(scope){
			return scope.page_info.must_not_haves
		},
		function(newValue, oldValue){
			var new_must_not_haves = [];
			for(var indexOfValue = 0;indexOfValue<newValue.length;indexOfValue++){
				var tag_index = 0;
				while($scope.page_info.tags.results[tag_index].id != newValue[indexOfValue]){
					tag_index = tag_index + 1;
				}
				new_must_not_haves.push($scope.page_info.tags.results[tag_index].name);
			}
			$scope.page_info.must_not_haves_name = new_must_not_haves;
		}
	);
});

mealApp.controller('FoodsListController', function($scope, Product){
	$scope.page_info = {
		'products': Product.get(),
		'message': "Our Food List"
	};

});


mealApp.config(function($routeProvider, $locationProvider){
    $routeProvider
    .when('/', {
        templateUrl: 'static/partials/taste_profile.html',
        controller: 'MealPlannerController'
    })
    .when('/foodsummary', {
        templateUrl: 'static/partials/foods_list.html',
        controller: 'FoodsListController'
    })
    .when('/suggestion', {
        templateUrl: 'static/partials/meal_suggestion.html'
    })
    .otherwise({
        redirectTo: '/'
    });
});