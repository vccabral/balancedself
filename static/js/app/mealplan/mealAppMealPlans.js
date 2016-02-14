var mealAppMealPlans = angular.module(
	'mealApp.MealPlans', [
		'mealApp.API',
		'ngRoute'
	]
);

mealAppMealPlans.controller('MealPlannerController', function($scope, Standard, Tag, MealPlan, Product, $timeout, $interval, $location) {
	$scope.page_info = {
		'tags': Tag.get(),
		'selected_standard': 0,
		'message': 'Design your Diet',
		'standards': Standard.get(),
		'products': Product.get(),
		'selected_span': 7,
		'mealplan': null,
		'failed_to_find_meal': false
	};

	$scope.setMeal = function(){
		$scope.page_info.standard_constraints = angular.copy($scope.page_info.standards.results[$scope.page_info.selected_standard-1].constraints_readonly);
	};

	var add_nutrient_params = function(params){
		for(var i=0;i<$scope.page_info.standard_constraints.length;i++){
			var d = $scope.page_info.standard_constraints[i];
			params['nutrient_'+d.nutrient.id+'_low'] = d.quantity;
			params['nutrient_'+d.nutrient.id+'_high'] = d.max_quantity;
		}
	};

	var get_exclusions = function(){
		var active_exclusions = _.filter($scope.page_info.tags.results, function(o) { return o.selected; });
		var named_arr_of_exclusions = _.map(active_exclusions, function(o){return o.name});
		return named_arr_of_exclusions;
	};

	var product_is_allowed = function(product, exclusions){
		var tags = _.map(product.tags, function(o){return o.name});
		var shared_tags = _.intersection(tags, exclusions);
		return shared_tags.length == 0;
	}

	var add_product_params = function(params){
		for(var i=0;i<$scope.page_info.products.results.length;i++){
			var product = $scope.page_info.products.results[i];
			var custom_span = product.custom_span;
			var span_multiplier = get_multiplier(custom_span, $scope.page_info.selected_span);
			var exclusions = get_exclusions();
			var product_allowed = product_is_allowed(product, exclusions);
			var product_allowed_multiplier = product_allowed ? 1 : 0;

			params['product_'+product.id+'_low'] = product.quantity * span_multiplier * product_allowed_multiplier;
			params['product_'+product.id+'_high'] = product.max_quantity * span_multiplier * product_allowed_multiplier;
		}
	};

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
	$scope.findOptimalMealPlan = function(){
		var params = {
			'mealplan': $scope.page_info.selected_standard,
			'span': $scope.page_info.selected_span
		};
		add_nutrient_params(params);
		add_product_params(params);
		var outside_mealplan = MealPlan.save(params, function(mealplan){
			$scope.page_info.mealplan = outside_mealplan;
			$scope.page_info.getting_meal_plan = false;
			$scope.page_info.failed_to_find_meal = !mealplan.success;
		});
	};
	$scope.get_product_index_by_id = function(id){
		return _.findIndex($scope.page_info.products.results, function(o) { return o.id == id; });
	}

});

mealAppMealPlans.config(function($routeProvider, $locationProvider, siteversion){
	$routeProvider
	.when('/mealplans', {
		templateUrl: 'static/js/app/mealplan/mealplan.html',
		controller: 'MealPlannerController'
	});
});