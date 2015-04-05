var mongoose = require('mongoose'),
    Schema = mongoose.Schema;

/**
 * Base Mongoose data model.
 */
function BaseSchema(options) {
  var that = new Schema(options);

  return that;
}

module.exports = BaseSchema;