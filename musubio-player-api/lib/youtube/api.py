from os import environ
from googleapiclient.discovery import build


DEVELOPER_KEY = environ['YOUTUBE_DEVELOPER_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


class YoutubeAPI():
    def __init__(self):
        self.api = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=DEVELOPER_KEY
        )

    def search(self, q, limit=25):
        """ YouTube Search """
        results = self.api.search().list(
            q=q,
            part='snippet',
            maxResults=limit).execute()

        videos = []
        channels = []
        playlists = []

        for result in results.get('items', []):
            if result['id']['kind'] == 'youtube#video':
                videos.append(result)
            elif result['id']['kind'] == "youtube#channel":
                channels.append("%s (%s)" % (result["snippet"]["title"],
                result["id"]["channelId"]))
            elif result['id']['kind'] == "youtube#playlist":
                playlists.append("%s (%s)" % (result["snippet"]["title"],
                result["id"]["playlistId"]))

        return results, videos, channels, playlists

    def video_list(self, id):
        """Get a list of videos by ID"""
        results = self.api.videos().list(
            id=id,
            part='snippet,contentDetails',
        ).execute()

        videos = []

        for result in results.get('items', []):
            if result['kind'] == 'youtube#video':
                videos.append(result)

        return results, videos