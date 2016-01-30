import endpoints
from protorpc import remote
from api import api_root

from lib.youtube.api import YoutubeAPI
from messages.youtube import ThumbnailMessage, VideoMessage, SearchResultsMessage, SearchRequestMessage

package = 'YouTube'


@api_root.api_class(resource_name='youtube')
class YouTubeApi(remote.Service):
    """YouTube API v1"""
    @endpoints.method(SearchRequestMessage,
                      SearchResultsMessage,
                      path='search',
                      http_method='GET',
                      name='search')
    def youtube_search(self, request):
        api = YoutubeAPI()
        results, videos, channels, playlists = api.search(request.q, request.limit)
        searchResults = SearchResultsMessage()

        items = []
        for item in videos:
            video = VideoMessage()
            video.id = item['id']['videoId']
            video.title = item['snippet']['title']
            video.url = 'https://www.youtube.com/watch?v=%s' % item['id']['videoId']
            video.channel_id = item['snippet']['channelId']
            video.published_at = item['snippet']['publishedAt']
            video.live_broadcast_content = item['snippet']['liveBroadcastContent']
            video.channel_title = item['snippet']['channelTitle']
            video.description = item['snippet']['description']

            thumbnail = ThumbnailMessage()
            thumbnail.default = item['snippet']['thumbnails']['default']['url']
            thumbnail.high = item['snippet']['thumbnails']['high']['url']
            thumbnail.medium = item['snippet']['thumbnails']['medium']['url']
            video.thumbnail = thumbnail

            items.append(video)

        """
        self.type = 'video'
        self.video_id = object['id']['videoId']
        self.video_url = 'https://www.youtube.com/watch?v=%s' % object['id']['videoId']
        self.title = snippet['title']
        self.channel_id = snippet['channelId']
        self.published_at = snippet['publishedAt']
        self.live_broadcast_content = snippet['liveBroadcastContent']
        self.channel_title = snippet['channelTitle']
        self.description = snippet['description']
        self.etag = object['etag']

        thumbnails = Object()
        thumbnails.default = snippet['thumbnails']['default']['url']
        thumbnails.high = snippet['thumbnails']['high']['url']
        thumbnails.medium = snippet['thumbnails']['medium']['url']
        self.thumbnails = thumbnails
        """

        searchResults.items = items

        return searchResults