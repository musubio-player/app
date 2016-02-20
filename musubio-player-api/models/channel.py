"""Helper model class for Musubio API.

Defines models for persisting and querying score data on a per user basis and
provides a method for returning a 401 Unauthorized when no current user can be
determined.
"""
from google.appengine.ext import ndb

from messages.channel import Channel as ChannelMessage
from models.video import VideoModel


TIME_FORMAT_STRING = '%b %d, %Y %I:%M:%S %p'

class ChannelModel(ndb.Model):
    """Model to store channels that have been inserted by users."""
    entity_id = ndb.IntegerProperty(required=True)
    title = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    videos = ndb.KeyProperty(kind=VideoModel, repeated=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def _get_kind(cls):
        return 'Channel'

    @property
    def timestamp(self):
        """Property to format a datetime object to string."""
        return self.created.strftime(TIME_FORMAT_STRING)

    def to_message(self):
        """Turns the Channel entity into a ProtoRPC object.

        This is necessary so the entity can be returned in an API request.

        Returns:
            An instance of Channel with the ID set to the datastore
            ID of the current entity, the outcome simply the entity's outcome value.
        """
        channel = ChannelMessage()
        channel.id = self.key.id()
        channel.entity_id = self.entity_id
        channel.title = self.title
        channel.description = self.description

        videos = []
        for video in self.videos:
            videos.append(video.get().to_message())

        channel.videos = videos
        channel.created = self.created
        channel.updated = self.updated

        return channel

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
        entity = cls(entity_id=message.entity_id, title=message.title, description=message.description)
        entity.put()
        return entity

    @classmethod
    def query_channels(cls):
        return cls.query()

    @classmethod
    def add_video(cls, message):
        # Get the entities.
        video = VideoModel.get_by_id(message.video_id)
        channel = cls.get_by_id(message.channel_id)

        # Add the video to the channel.
        channel.videos.append(video.key)
        channel.put()

        return channel

    @classmethod
    def remove_video(cls):
        pass