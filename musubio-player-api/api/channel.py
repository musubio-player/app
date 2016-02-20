"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""
import endpoints, logging
from protorpc import message_types
from protorpc import remote
from api import api_root

from google.appengine.api import memcache

from messages.channel import Channel, ChannelInsertRequest, ChannelListResponse, ChannelDetailsRequest, ChannelAddVideoRequest
from models.channel import ChannelModel

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
        logging.info('channel_details()')

        cache_key = 'channels/details/%s' % request.id
        channel = memcache.get(cache_key)
        if channel is None:
            channel = ChannelModel.get_details(request)

            # Cache results
            memcache.add(cache_key, channel)

            logging.info('Channel details cached')
        else:
            logging.info('Channel details read from cache')


        return channel.to_message()

    @endpoints.method(message_types.VoidMessage,
                      ChannelListResponse,
                      path='channels',
                      http_method='GET',
                      name='channels.list')
    def channel_list(self, request):
        logging.info('channel_list()')

        cache_key = 'channels/list'
        channels = memcache.get(cache_key)
        if channels is None:
            query = ChannelModel.query_channels()
            channels = [entity.to_message() for entity in query.fetch()]

            # Cache results
            memcache.add(cache_key, channels)

            logging.info('Channel list cached')
        else:
            logging.info('Channel list read from cache')

        channelList = ChannelListResponse()
        channelList.channels = channels

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