"""ProtoRPC message class definitions for Musubio API."""

from protorpc import messages

from messages.channel import Channel, ChannelBatchImportRequest


class Importer(messages.Message):
    channels = messages.MessageField(Channel, 1, repeated=True)


class ImporterBatchRequest(messages.Message):
    channels = messages.MessageField(ChannelBatchImportRequest, 1, repeated=True)

