"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""
import endpoints
from protorpc import message_types
from protorpc import remote
from api import api_root

from messages.channel import Channel, ChannelInsertRequest, ChannelListResponse, ChannelDetailsRequest, ChannelAddVideoRequest
from models.channel import Channel as ChannelModel

package = 'Musubio'


@api_root.api_class(resource_name='musubio')
class ChannelApi(remote.Service):
    """Musubio Channel API v1"""
    @endpoints.method(ChannelDetailsRequest,
                      Channel,
                      path='channels/{id}',
                      http_method='GET',
                      name='channels.details')
    def channel_details(self, request):
        channel = ChannelModel.get_details(request)
        return channel.to_message()

    @endpoints.method(message_types.VoidMessage,
                      ChannelListResponse,
                      path='channels',
                      http_method='GET',
                      name='channels.list')
    def channel_list(self, request):
        query = ChannelModel.query_channels()
        items = [entity.to_message() for entity in query.fetch()]

        channelList = ChannelListResponse()
        channelList.items = items

        return channelList

    @endpoints.method(ChannelInsertRequest,
                      Channel,
                      path='channels',
                      http_method='POST',
                      name='channels.insert')
    def channel_insert(self, request):
        entity = ChannelModel.put_from_message(request)
        return entity.to_message()

    @endpoints.method(ChannelAddVideoRequest,
                        Channel,
                        path='channels/add/video',
                        http_method='POST',
                        name='channels.addPost')
    def channel_add_post(self, request):
        channel = ChannelModel.add_video(request)
        return channel.to_message()