var mongoose = require('mongoose'),
    BaseSchema = require('./base');

function ChatSchema(options) {
  var that = new BaseSchema(options);

  that.add({
    id: Number,
    username: String,
    body: String,
    room_id: Number,
    youtube_id: String,
    video_timestamp: Number,
    post_date: Date,
  });

  return that;
}

module.exports = mongoose.model('MusubioChat', ChatSchema(), 'chats');