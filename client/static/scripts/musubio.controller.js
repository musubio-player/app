musubio.controller('HomePageController', ['$scope', '$http', function($scope, $http) {
  $scope.init = function() {
    $scope.getChannels();
  }

  $scope.getChannels = function() {
    $http.get('http://local.core.musubio.com/api/channels/').
      success(function(data, status, headers, config) {
        $scope.channels = data;
      }).
      error(function(data, status, headers, config) {

      });
  }

  $scope.init();
}]);

musubio.controller('ChannelController', ['$scope', '$http', '$routeParams', function($scope, $http, $routeParams) {
  $scope.init = function() {
    var channelId = $routeParams.slug;

    $scope.getChannels();
    $scope.getChannel(channelId);
    $scope.getActivityStream(channelId);
  }

  $scope.getChannel = function(channelId) {
    $http.get('http://local.core.musubio.com/api/channels/' + channelId).
      success(function(data, status, headers, config) {
        $scope.channel = data;

        var now = new Date();
        var startTime = new Date('2015-04-05T06:00:00.043Z');
        // startTime = new Date(startTime.setMinutes(0));
        // startTime = new Date(startTime.setSeconds(0));

        var duration = $scope.channel.posts[0].post.duration;
        var jumpToTime = Math.floor(((now.getTime() - startTime.getTime()) % duration) / 1000);

        $scope.videoEmbed = '<iframe width="750" height="422" src="https://www.youtube.com/embed/' + $scope.channel.posts[0].post.youtube_id + '?autoplay=1&controls=1&loop=1&start=' + jumpToTime + '" frameborder="0" allowfullscreen></iframe>'
      }).
      error(function(data, status, headers, config) {

      });
  }

  $scope.getChannels = function() {
    $http.get('http://local.core.musubio.com/api/channels/').
      success(function(data, status, headers, config) {
        $scope.channels = data;
      }).
      error(function(data, status, headers, config) {

      });
  }

  $scope.getActivityStream = function(channelId) {
    $scope.stream = [
      {
        type: 'chat',
        user: { username: 'buster.posey', avatar: 'http://placehold.it/50x50' },
        post: {
          body: 'Li Europan lingues es membres del sam familie. Lor separat existentie es un myth. Por scientie, musica, sport etc, litot Europa usa li sam vocabular.',
          date_published: new Date(),
        },
      },
      {
        type: 'chat',
        user: { username: 'brandon.belt', avatar: 'http://placehold.it/50x50' },
        post: {
          body: 'Li lingues differe solmen in li grammatica, li pronunciation e li plu commun vocabules.',
          date_published: new Date(),
        },
      },
      {
        type: 'chat',
        user: { username: 'angel.pagan', avatar: 'http://placehold.it/50x50' },
        post: {
          body: 'A un Angleso it va semblar un simplificat Angles, quam un skeptic Cambridge amico dit me que Occidental es. Li Europan lingues es membres del sam familie.',
          date_published: new Date(),
        },
      },
      {
        type: 'system',
        user: { username: 'matt.cain', avatar: 'http://placehold.it/50x50' },
        post: {
          body: 'has entered the channel.',
          date_published: new Date(),
        },
      },
      {
        type: 'chat',
        user: { username: 'matt.cain', avatar: 'http://placehold.it/50x50' },
        post: {
          body: 'Omnicos directe al desirabilite de un nov lingua franca: On refusa continuar payar custosi traductores.',
          date_published: new Date(),
        },
      },
    ];
  }

  $scope.init();
}]);