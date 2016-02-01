import endpoints
from protorpc import remote
from api import api_root

from lib.youtube.api import YoutubeAPI
from messages.youtube import ThumbnailMessage, Video, SearchResultsMessage, SearchRequestMessage, VideoList, VideoListRequestMessage

package = 'YouTube'


@api_root.api_class(resource_name='youtube')
class YouTubeApi(remote.Service):
    """YouTube API v1"""
    @endpoints.method(SearchRequestMessage,
                      SearchResultsMessage,
                      path='youtube/search',
                      http_method='GET',
                      name='youtube.search')
    def youtube_search(self, request):
        api = YoutubeAPI()
        results, videos, channels, playlists = api.search(request.q, request.limit)
        searchResults = SearchResultsMessage()

        results = []
        for item in videos:
            video = YouTubeApi.to_message(item)
            results.append(video)

        searchResults.videos = results

        return searchResults

    @endpoints.method(VideoListRequestMessage,
                      VideoList,
                      path='youtube/videos/list',
                      http_method='GET',
                      name='youtube.videos.list')
    def youtube_video_list(self, request):
        """
        Fetches a list of YouTube videos by ID.

        :param request:
        :return:
        """
        api = YoutubeAPI()
        results, videos = api.video_list(request.id)

        videoList = []
        for item in videos:
            video = YouTubeApi.to_message(item)
            videoList.append(video)

        videoListMessage = VideoList()
        videoListMessage.videos = videoList

        return videoListMessage

    @staticmethod
    def to_message(video):
        """
        Converts the JSON returned from the YouTube API to a Video message.

        :param video: JSON data of a video.
        :return: Video message data object.
        """
        videoMessage = Video()

        # ID's are in various structures in the YouTube JSON data.
        try:
            id = video['id']['videoId']
        except:
            id = video['id']

        videoMessage.id = id
        videoMessage.title = video['snippet']['title']
        videoMessage.url = 'https://www.youtube.com/watch?v=%s' % id
        videoMessage.channel_id = video['snippet']['channelId']
        videoMessage.published_at = video['snippet']['publishedAt']
        videoMessage.live_broadcast_content = video['snippet']['liveBroadcastContent']
        videoMessage.channel_title = video['snippet']['channelTitle']
        videoMessage.description = video['snippet']['description']

        thumbnail = ThumbnailMessage()
        thumbnail.default = video['snippet']['thumbnails']['default']['url']
        thumbnail.high = video['snippet']['thumbnails']['high']['url']
        thumbnail.medium = video['snippet']['thumbnails']['medium']['url']
        videoMessage.thumbnail = thumbnail

        return videoMessage