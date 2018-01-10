var bundesApp = angular.module('bundesApp', ['chart.js']);

bundesApp.controller('mainCtrl', function mainCtrl($scope) {
  //$scope.states = get_states();
  $scope.states = get_states();
  $scope.input = {
    filter: ""
  };

  $scope.change_active_state = function(s){
    $scope.active_state = s;
    $scope.input.filter = ""
    $scope.list_regions();
  }

  $scope.change_active_region = function(r){
    $scope.active_region = r;
    var results = get_results(r.id);
    results = prepare_results(results);
    $scope.result = results[0];
    $scope.prepare_diagram(results[1]);
  }

  $scope.list_regions = function(){
    $scope.regions = filter_regions(get_regions($scope.active_state.id), $scope.input.filter);
    $scope.active_region = null;
  }

  $scope.prepare_diagram = function(results){
    $scope.parties = results[0];
    $scope.type = ['Erststimmen', 'Zweitstimmen'];

    $scope.data = [
        results[1],
        results[2]
    ];
  }


});

var filter_regions = function(regions, filter) {
    temp = [];
    for(i = 0; i < regions.length; i ++){
        if(regions[i].name.includes(filter)){
            temp.push(regions[i]);
        }
    }
    return temp;
}

var prepare_results = function(result){
    category = [];
    first = [];
    second = [];
    for(i = 0; i < result.length; i++) {
        if(result[i].category_id > 4){
            name = get_category_name(result[i].category_id).name;
            category.push(name);
            if (result[i].vote_type === "Erststimmen"){
                first.push(result[i].priorPeriodVotes);
            } else {
                second.push(result[i].priorPeriodVotes);
            }
        }
    }
    category = category.filter(function(item, i, ar){ return ar.indexOf(item) === i; });

    arr1 = [];
    arr2 = [category, first, second];
    for(i = category.length - 1; i >= 0; i--) {
        if(first[i] > 0 || second[i] > 0){
            arr1.push([category[i], first[i], second[i]]);
        }
        if(first[i] == 0 && second[i] == 0) {
            arr2[0].splice(i, 1);
            arr2[1].splice(i, 1);
            arr2[2].splice(i, 1);
        }
    }
    console.log(arr2);
    arr = [arr1, arr2];
    return arr;
}

var get_states = function() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/states", false);
    xhttp.send();
    return JSON.parse(xhttp.responseText);
}

var get_regions = function(id) {
    var address = "/region/" + id + "/constituencies"
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", address, false);
    xhttp.send();
    return JSON.parse(xhttp.responseText);
}

var get_results = function(id) {
    var address = "/region/" + id + "/voteResults"
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", address, false);
    xhttp.send();
    return JSON.parse(xhttp.responseText);
}

var get_category_name = function(id) {
    var address = "/category/" + id
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", address, false);
    xhttp.send();
    return JSON.parse(xhttp.responseText);
}