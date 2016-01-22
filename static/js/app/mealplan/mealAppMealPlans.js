var mealAppMealPlans = angular.module(
	'mealApp.MealPlans', [
		'mealApp.API',
		'ngRoute'
	]
);

mealAppMealPlans.controller('MealPlannerController', function($scope, Standard, Tag, MealPlan, Product, $timeout, $interval) {

	$scope.should_show_product = function(product){
		var found_all_required = true;
		if($scope.page_info.required_tags.$resolved){
			for(var lcv=0;lcv<$scope.page_info.required_tags.results.length;lcv++){
				if($scope.page_info.required_tags.results[lcv].selected){
					var product_tag_lcv = 0;
					var tag_name = $scope.page_info.required_tags.results[lcv].name;
					while(product_tag_lcv < product.tags.length && tag_name != product.tags[product_tag_lcv].name){product_tag_lcv++;}
					found_all_required = found_all_required && product_tag_lcv < product.tags.length;
				}
			}
		}

		var does_not_contain_exclude = true;
		if($scope.page_info.exclude_tags.$resolved){
			for(var lcv=0;lcv<$scope.page_info.exclude_tags.results.length;lcv++){
				if($scope.page_info.exclude_tags.results[lcv].selected){
					var product_tag_lcv = 0;
					var tag_name = $scope.page_info.exclude_tags.results[lcv].name;
					while(product_tag_lcv < product.tags.length && tag_name != product.tags[product_tag_lcv].name){product_tag_lcv++;}
					does_not_contain_exclude = does_not_contain_exclude && product_tag_lcv == product.tags.length;
				}
			}
		}

		var has_one_desired_trait = true;
		if($scope.page_info.desired_tags.$resolved){
			var has_one_desired_trait = false;
			var desired_tags = [];
			for(var lcv=0;lcv<$scope.page_info.desired_tags.results.length;lcv++){
				if($scope.page_info.desired_tags.results[lcv].selected){
					desired_tags.push($scope.page_info.desired_tags.results[lcv].name);
				}
			}
			var lcv = 0;
			while(lcv < product.tags.length && desired_tags.indexOf(product.tags[lcv].name)==-1){lcv++;}
			has_one_desired_trait = lcv < product.tags.length;
		}

		return found_all_required && does_not_contain_exclude && has_one_desired_trait;
	}
	$scope.greaterThan = function(prop, val){
	    return function(item){
			return item[prop] > val;
	    }
	};

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

		var get_multiplier = function(k, span){
			if(k=='none'){
				return 0;
			}
			else if(k=='entire'){ //works
				return 1.0 / span;
			}
			else if(k=='daily'){ //works
				return 1.0;
			}
			else if(k=='weekly'){
				return 1 / 7.0;
			}
			else if(k=='monthly'){
				return 1 / 28.0;
			}
			else{
				return 1;
			}
		}

		for(var i=0;i<$scope.page_info.products.results.length;i++){
			var d = $scope.page_info.products.results[i];
			var custom_span = $scope.page_info.products.results[i].custom_span;
			var span_multiplier = get_multiplier(custom_span, $scope.page_info.selected_span);
			var product_allowed = $scope.should_show_product($scope.page_info.products.results[i]);

			if(product_allowed){
				params['product_'+d.id+'_low'] = d.quantity * span_multiplier;
				params['product_'+d.id+'_high'] = d.max_quantity * span_multiplier;
			}else{
				params['product_'+d.id+'_low'] = 0;
				params['product_'+d.id+'_high'] = 0;
			}
		}

		$scope.page_info.mealplan = MealPlan.save(params, function(mealplan){
			$scope.page_info.getting_meal_plan = false;
			$scope.page_info.failed_to_find_meal = !mealplan.success;
		});
	};
	$scope.findOptimalMealPlan = function(){
		$scope.findOptimalMealPlanBrains();
	};
	$scope.setMeal = function(){
		$scope.page_info.standard_constraints = angular.copy($scope.page_info.standards.results[$scope.page_info.selected_standard-1].constraints_readonly);
	};

	$scope.page_info = {
		'message': 'Design your Diet',
		'standards': Standard.get(),
		'tags': Tag.get(),
		'required_tags': Tag.get(),
		'desired_tags': Tag.get(),
		'exclude_tags': Tag.get(),
		'products': Product.get(),
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
		'selected_span': 7,
		'show_all_food': true,
		'selection_options': [{ "value": 'day', "text": "Daily" }, { "value": 'week', "text": "Weekly" }],
		'spans': [1,2,7,14,21,28,31,60,90,365]
	};
});


mealAppMealPlans.config(function($routeProvider, $locationProvider){
    $routeProvider
    .when('/mealplans', {
        templateUrl: 'static/js/app/mealplan/mealplan.html',
        controller: 'MealPlannerController'
    })
});