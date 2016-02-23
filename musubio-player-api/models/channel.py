"""Helper model class for Musubio API.

Defines models for persisting and querying score data on a per user basis and
provides a method for returning a 401 Unauthorized when no current user can be
determined.
"""
import time, datetime, logging

from google.appengine.ext import ndb
from google.appengine.api import memcache

from messages.channel import Channel as ChannelMessage
from models.video import VideoModel


DATETIME_FORMAT_STRING = '%Y-%m-%dT%H:%M:%S.%f'

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

    def to_message(self, current=False):
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

        if current is True:
            # Get only the current video that is playing.
            videos.append(self.get_current_video())
        else:
            # Get all the videos on this channel.
            for video in self.videos:
                cache_key = 'video:get:%s' % (video.id)
                video_data = memcache.get(cache_key)
                if video_data is None:
                    video_data = video.get().to_message()

                    # Cache results
                    memcache.add(cache_key, video_data)
                    logging.info('[CACHE ADD] Video: %s' % video)
                else:
                    logging.info('[CACHE READ] Video: %s' % video)

                videos.append(video_data)

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
    def get_channels(cls):
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

    def get_current_video(self):
        """
        Calculates what the current video that is playing.

        :return: Video
        """
        now = int(time.time())
        base_time = int(time.mktime(self.created.timetuple()))
        # now = Math.floor(new Date('Wed Feb 04 2016 06:03:20 GMT-0800 (PST)').getTime() / 1000)
        # baseTime = Math.floor(new Date('Wed Feb 04 2016 06:00:00 GMT-0800 (PST)').getTime() / 1000)

        time_since_base_time = now - base_time

        print '*=====================================================*'
        print 'now: %s' % now
        print 'base_time: %s' % base_time
        print 'time_since_base_time: %s' % time_since_base_time

        # playlist_start_time = time_since_base_time % that.playlistTotalDuration
        # curr_duration = 0
        # video_index = 0
        # start_time = 0
        #
        # for index, video in self.videos.iteritems():
        #   if playlist_start_time >= curr_duration:
        #     video_index = index
        #     start_time = playlist_start_time - curr_duration
        #
        #   curr_duration += curr_duration + int(video.duration)

        return self.videos[0].get().to_message()