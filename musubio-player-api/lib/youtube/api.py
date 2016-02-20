import math
from os import environ
from googleapiclient.discovery import build


DEVELOPER_KEY = environ['YOUTUBE_DEVELOPER_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_API_VIDEO_LIST_LIMIT = 50

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

    def video_list(self, video_ids):
        """Get a list of videos by ID"""
        results = None
        videos = []

        iterations = int(math.ceil(len(video_ids) / float(YOUTUBE_API_VIDEO_LIST_LIMIT)))

        print 'ID LIST LENGTH: %s' % len(video_ids)
        print 'iterations: %s' % iterations

        offset = 0
        limit = YOUTUBE_API_VIDEO_LIST_LIMIT
        for index in range(offset, iterations):
            # Set current batch of video IDs to request.
            ids = ','.join(video_ids[offset:limit])

            # Call the YouTube API for the video data.
            results = self.api.videos().list(
                id=ids,
                part='snippet,contentDetails',
            ).execute()

            for result in results.get('items', []):
                if result['kind'] == 'youtube#video':
                    videos.append(result)

            # Set the next iteration parameters.
            offset = (index + 1) * YOUTUBE_API_VIDEO_LIST_LIMIT
            limit = offset + YOUTUBE_API_VIDEO_LIST_LIMIT

        return results, videos