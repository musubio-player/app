import endpoints, logging
from protorpc import remote
from api import api_root

from messages.importer import ImporterBatchRequest, Importer, ImporterChannelRequest
from messages.channel import ChannelAddVideoRequest, Channel
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
        for channel in request.channels:
            self.sync_channel(channel)

        logging.info('[IMPORT Completed')

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

        results, videos = api.video_list(video_ids)

        # Put the video data in a dictionary keyed by the video ID.
        for video in videos:
            videoMessage = YouTubeEndpoint.to_message(video)
            video_dict[videoMessage.id] = videoMessage

        return video_dict

    @endpoints.method(ImporterChannelRequest,
                      Importer,
                      path='importer/channel',
                      http_method='POST',
                      name='importer.channel')
    def import_channel(self, request):
        """
        Imports channel data from a JSON file.

        :param request:
        :return:
        """
        self.sync_channel(request)

        return Importer()

    def sync_channel(self, channel):
        # Check if the channel exists.
        channel_query = ChannelModel.query(ChannelModel.entity_id == channel.entity_id)
        channel_instance = channel_query.get()

        if channel_instance is None:
            # Create new channel instance to save.
            channel_instance = ChannelModel()
            logging.info('[CREATED] Channel: %s' % channel.title)
        else:
            logging.info('[UPDATED] Channel: %s' % channel.title)

        # Save/update the channel.
        channel_instance.entity_id = channel.entity_id
        channel_instance.title = channel.title
        channel_instance.description = channel.description
        channel_instance.videos = [] # Refresh videos.
        channel_instance.put()

        # Create a list of video ID's to fetch video data from YouTube.
        video_ids = []
        for video in channel.videos:
            video_ids.append(video.video_id)

        # Get video data.
        video_dict = ImporterApi.get_video_data(video_ids)

        for video_id, video_data in video_dict.iteritems():
            # Check that video does not exist locally before saving.
            query = VideoModel.query(VideoModel.video_id == video_id)
            video_instance = query.get()

            if video_instance is None:
                video_instance = VideoModel()

                # Add the video.
                video_instance.title = video_data.title
                video_instance.description = video_data.description
                video_instance.video_id = video_id
                video_instance.duration_ISO = video_data.duration_ISO
                video_instance.duration = video_data.duration
                video_instance.put()
                logging.info('[CREATED] Video: %s' % video_data.title)
            else:
                logging.info('[EXISTS] Video: %s' % video_data.title)

            # Add the video to the channel.
            message = ChannelAddVideoRequest()
            message.channel_id = channel_instance.key.id()
            message.video_id = video_instance.key.id()
            channel_instance.add_video(message)
