"""ProtoRPC message class definitions for Musubio API."""

from protorpc import messages, message_types
from messages.video import Video


class Channel(messages.Message):
    """Channel that stores a message."""
    id = messages.IntegerField(1, required=True)
    title = messages.StringField(2, required=True)
    description = messages.StringField(3, required=False)
    videos = messages.MessageField(Video, 4, repeated=True)
    created = message_types.DateTimeField(5, required=False)
    updated = message_types.DateTimeField(6, required=False)


class ChannelDetailsRequest(messages.Message):
    """ProtoRPC message definition to represent a channel to be fetched."""
    id = messages.IntegerField(1, required=True)


class ChannelInsertRequest(messages.Message):
    """ProtoRPC message definition to represent a channel to be inserted."""
    title = messages.StringField(1, required=True)
    description = messages.StringField(2, required=False)


class ChannelListResponse(messages.Message):
    """Collection of Channels."""
    items = messages.MessageField(Channel, 1, repeated=True)


class ChannelAddVideoRequest(messages.Message):
    """ProtoRPC message definition to represent a videos to be added to a channel."""
    channel_id = messages.IntegerField(1, required=True)
    video_id = messages.IntegerField(2, required=True)