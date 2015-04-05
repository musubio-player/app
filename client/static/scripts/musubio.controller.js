musubio.controller('HomePageController', ['$scope', '$http', function($scope, $http) {
  $scope.init = function() {
    $scope.getRooms();
  }

  $scope.getRooms = function() {
    $http.get('http://local.core.musubio.com/api/rooms/').
      success(function(data, status, headers, config) {
        $scope.rooms = data;
      }).
      error(function(data, status, headers, config) {

      });
  }

  $scope.init();
}]);

musubio.controller('RoomController', ['$scope', '$http', '$routeParams', function($scope, $http, $routeParams) {
  $scope.init = function() {
    var roomId = $routeParams.slug;

    $scope.getRooms();
    $scope.getRoom(roomId);
    $scope.getActivityStream(roomId);
  }

  $scope.getRoom = function(roomId) {
    $http.get('http://local.core.musubio.com/api/rooms/' + roomId).
      success(function(data, status, headers, config) {
        $scope.room = data;

        var now = new Date();
        var startTime = new Date('2015-04-05T06:00:00.043Z');
        // startTime = new Date(startTime.setMinutes(0));
        // startTime = new Date(startTime.setSeconds(0));

        var duration = $scope.room.posts[0].post.duration;
        var jumpToTime = Math.floor(((now.getTime() - startTime.getTime()) % duration) / 1000);

        $scope.videoEmbed = '<iframe width="750" height="422" src="https://www.youtube.com/embed/' + $scope.room.posts[0].post.youtube_id + '?autoplay=1&controls=1&loop=1&start=' + jumpToTime + '" frameborder="0" allowfullscreen></iframe>'
      }).
      error(function(data, status, headers, config) {

      });
  }

  $scope.getRooms = function() {
    $http.get('http://local.core.musubio.com/api/rooms/').
      success(function(data, status, headers, config) {
        $scope.rooms = data;
      }).
      error(function(data, status, headers, config) {

      });
  }

  $scope.getActivityStream = function(roomId) {
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
          body: 'has entered the room.',
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