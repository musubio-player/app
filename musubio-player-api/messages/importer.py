"""ProtoRPC message class definitions for Musubio API."""

from protorpc import messages, message_types

from messages.channel import Channel, ChannelBatchImportRequest
from messages.video import VideoImportRequest


class Importer(messages.Message):
    channels = messages.MessageField(Channel, 1, repeated=True)


class ImporterBatchRequest(messages.Message):
    channels = messages.MessageField(ChannelBatchImportRequest, 1, repeated=True)


class ImporterChannelRequest(messages.Message):
    entity_id = messages.IntegerField(1, required=True)
    title = messages.StringField(2, required=True)
    description = messages.StringField(3, required=False)
    videos = messages.MessageField(VideoImportRequest, 4, repeated=True)

