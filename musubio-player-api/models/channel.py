"""Helper model class for Musubio API.

Defines models for persisting and querying score data on a per user basis and
provides a method for returning a 401 Unauthorized when no current user can be
determined.
"""
from google.appengine.ext import ndb

from messages.channel import ChannelResponseMessage


TIME_FORMAT_STRING = '%b %d, %Y %I:%M:%S %p'

class Channel(ndb.Model):
    """Model to store channels that have been inserted by users."""
    title = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now_add=True)

    @property
    def timestamp(self):
        """Property to format a datetime object to string."""
        return self.created.strftime(TIME_FORMAT_STRING)

    def to_message(self):
        """Turns the Channel entity into a ProtoRPC object.

        This is necessary so the entity can be returned in an API request.

        Returns:
            An instance of ChannelResponseMessage with the ID set to the datastore
            ID of the current entity, the outcome simply the entity's outcome value.
        """
        channelMessage = ChannelResponseMessage()
        channelMessage.id = self.key.id()
        channelMessage.title = self.title
        channelMessage.description = self.description
        channelMessage.created = self.created
        channelMessage.updated = self.updated

        return channelMessage

    @classmethod
    def get_details(cls, message):
        return cls.get_by_id(message.id)

    @classmethod
    def put_from_message(cls, message):
        """Gets the current user and inserts a channel.

        Args:
            message: A ChannelRequestMessage instance to be inserted.

        Returns:
            The Channel entity that was inserted.
        """
        # current_user = get_endpoints_current_user()
        # entity = cls(outcome=message.outcome, player=current_user)
        entity = cls(title=message.title, description=message.description)
        entity.put()
        return entity

    @classmethod
    def query_channels(cls):
        return cls.query()