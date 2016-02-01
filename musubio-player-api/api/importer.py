import endpoints, logging
from protorpc import remote
from api import api_root

from messages.importer import ImporterBatchRequest, Importer
from messages.channel import ChannelAddVideoRequest
from models.channel import ChannelModel
from models.video import VideoModel
from models.importer import Importer as ImporterModel
from youtube import YoutubeAPI
from api.youtube import YouTubeApi as YouTubeEndpoint

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
        """
        Import Musubio channels and playlist videos from a JSON string.

        :param request:
        :return:
        """
        logging.info('import_init() called')

        # Extract the video IDs from the data to fetch video details from YouTube.
        video_ids = ImporterApi.get_video_ids(request.channels)
        video_dict = ImporterApi.get_video_data(video_ids)

        # Clear out the existing records.
        logging.info('Clearing out channel and video data')
        ImporterModel.delete_all(ChannelModel)
        ImporterModel.delete_all(VideoModel)

        logging.info('Iterating through JSON data to import')
        for channel in request.channels:
            logging.info('Creating channel')

            # Create the channel.
            channelInstance = ChannelModel()
            channelInstance.title = channel.title
            channelInstance.description = channel.description
            channelInstance.put()

            # Create videos and associate them to the channel.
            for video in channel.videos:
                logging.info('Creating video')

                videoInstance = VideoModel()

                # Get video data from YouTube.
                video_data = video_dict[video.video_id]

                videoInstance.title = video_data.title
                videoInstance.description = video_data.description
                videoInstance.video_id = video.video_id
                videoInstance.put()

                message = ChannelAddVideoRequest()
                message.channel_id = channelInstance.key.id()
                message.video_id = videoInstance.key.id()
                channelInstance.add_video(message)

        importer = Importer()

        return importer

    @staticmethod
    def get_video_ids(channels):
        """
        Gets all the video ID's that are to be imported.

        :param channel: JSON data of the channel and videos to be imported.
        :return:
        """
        logging.info('get_video_ids() called')

        video_ids = []
        for channel in channels:
            for video in channel.videos:
                video_ids.append(video.video_id)

        return set(video_ids)

    @staticmethod
    def get_video_data(video_ids):
        """
        Gets the video data via the YouTube API.
        :param video_ids:
        :return: a dictionary of videos keyed by the YouTube ID.
        """
        logging.info('get_video_data() called')

        video_dict = {}

        api = YoutubeAPI()
        results, videos = api.video_list(",".join(video_ids))

        # Put the video data in a dictionary keyed by the video ID.
        for video in videos:
            videoMessage = YouTubeEndpoint.to_message(video)
            video_dict[videoMessage.id] = videoMessage

        return video_dict


