"""ProtoRPC message class definitions for Musubio API."""

from protorpc import messages, message_types


class Image(messages.Message):
    """Video image data object."""
    default = messages.StringField(1, required=True)
    high = messages.StringField(2, required=True)
    medium = messages.StringField(3, required=True)


class Video(messages.Message):
    """Video data object."""
    id = messages.IntegerField(1, required=True)
    video_id = messages.StringField(2, required=True)
    title = messages.StringField(3, required=True)
    description = messages.StringField(4, required=True)
    image = messages.MessageField(Image, 5, required=True)
    created = message_types.DateTimeField(6, required=True)


class VideoInsertRequest(messages.Message):
    """ProtoRPC message definition to represent a video to be inserted."""
    title = messages.StringField(1, required=True)
    description = messages.StringField(2, required=True)
    video_id = messages.StringField(3, required=True)


class VideoImportRequest(messages.Message):
    """ProtoRPC message definition to represent a video to be imported."""
    video_id = messages.StringField(1, required=True)


class VideoList(messages.Message):
    """Collection of Videos."""
    videos = messages.MessageField(Video, 1, repeated=True)
