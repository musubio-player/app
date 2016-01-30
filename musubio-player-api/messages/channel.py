"""ProtoRPC message class definitions for Musubio API."""

from protorpc import messages, message_types
from messages.video import VideoList


class ChannelResponseMessage(messages.Message):
    """Channel that stores a message."""
    id = messages.IntegerField(1, required=True)
    title = messages.StringField(2, required=True)
    description = messages.StringField(3, required=False)
    videos = messages.MessageField(VideoList, 4)
    created = message_types.DateTimeField(5, required=False)
    updated = message_types.DateTimeField(6, required=False)


class ChannelDetailsRequestMessage(messages.Message):
    """ProtoRPC message definition to represent a channel to be fetched."""
    id = messages.IntegerField(1, required=True)


class ChannelRequestMessage(messages.Message):
    """ProtoRPC message definition to represent a channel to be inserted."""
    title = messages.StringField(1, required=True)
    description = messages.StringField(2, required=False)


class ChannelListResponse(messages.Message):
    """Collection of Channels."""
    items = messages.MessageField(ChannelResponseMessage, 1, repeated=True)