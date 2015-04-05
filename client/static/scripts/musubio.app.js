var musubio = angular.module('musubio', ['ngRoute'])

.config(function($routeProvider) {
  $routeProvider
    .when('/', {
      controller: 'HomePageController',
      templateUrl: 'home.html',
    })
    .when('/channels/:slug', {
      controller: 'ChannelController',
      templateUrl: 'channel.html',
    })
    .otherwise({
      redirectTo:'/'
    });
})

.filter('unsafe', function($sce) {
  return function(val) {
    return $sce.trustAsHtml(val);
  };
});