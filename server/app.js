var express = require('express'),
    app = express();

var mode = process.env.NODE_ENV ? process.env.NODE_ENV : 'local';
var config = require('./config/' + mode);

app.get('/chat/', function (req, res) {
  res.send('Hello World!');
});

app.put('/chat/', function (req, res) {
  res.send('Hello World!');
});

var server = app.listen(3000, function () {

  var host = server.address().address;
  var port = server.address().port;

  console.log('Example app listening at http://%s:%s', host, port);

});