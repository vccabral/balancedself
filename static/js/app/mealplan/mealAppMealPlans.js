var mealAppMealPlans = angular.module(
	'mealApp.MealPlans', [
		'mealApp.API',
		'ngRoute'
	]
);


mealAppMealPlans.controller('MealPlannerController', function($scope, Standard, Tag, MealPlan, $timeout, $interval) {
	$scope.greaterThan = function(prop, val){
	    return function(item){
	      return item[prop] > val;
	    }
	};

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
		$scope.page_info.getting_meal_plan = true;
		$scope.page_info.failed_to_find_meal = false;
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

		for(var i=0;i<$scope.page_info.product_constraints.length;i++){
			var d = $scope.page_info.product_constraints[i];
			params['product_'+d.product.id+'_low'] = d.quantity;
			params['product_'+d.product.id+'_high'] = d.max_quantity;
		}

		$scope.page_info.mealplan = MealPlan.get(params, function(mealplan){
			$scope.page_info.getting_meal_plan = false;
			$scope.page_info.failed_to_find_meal = !mealplan.success;
		});
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
		'getting_meal_plan': false,
		'failed_to_find_meal': false,
		'standard_constraints': [],
		'product_constraints': {},
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


mealAppMealPlans.config(function($routeProvider, $locationProvider){
    $routeProvider
    .when('/mealplans', {
        templateUrl: 'static/js/app/mealplan/mealplan.html',
        controller: 'MealPlannerController'
    })
});