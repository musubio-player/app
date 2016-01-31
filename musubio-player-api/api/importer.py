import endpoints
from protorpc import remote
from api import api_root

from messages.importer import ImporterBatchRequest, Importer
from messages.channel import ChannelAddVideoRequest
from models.channel import ChannelModel
from models.video import VideoModel
from models.importer import Importer as ImporterModel

package = 'Musubio'


@api_root.api_class(resource_name='musubio')
class ImporterApi(remote.Service):
    """Musubi Data Import API v1"""
    @endpoints.method(ImporterBatchRequest,
                      Importer,
                      path='importer',
                      http_method='POST',
                      name='importer.init')
    def import_init(self, request):
        # Clear out the existing records.
        ImporterModel.delete_all(ChannelModel)
        ImporterModel.delete_all(VideoModel)

        for channel in request.channels:
            # Create the channel.
            channelInstance = ChannelModel()
            channelInstance.title = channel.title
            channelInstance.description = channel.description
            channelInstance.put()

            # Create videos and associate them to the channel.
            for video in channel.videos:
                videoInstance = VideoModel()
                videoInstance.title = video.title
                videoInstance.description = video.description
                videoInstance.video_id = video.video_id
                videoInstance.put()

                message = ChannelAddVideoRequest()
                message.channel_id = channelInstance.key.id()
                message.video_id = videoInstance.key.id()
                channelInstance.add_video(message)

        importer = Importer()

        return importer