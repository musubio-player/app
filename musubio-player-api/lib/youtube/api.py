from googleapiclient.discovery import build


#DEVELOPER_KEY = "AIzaSyDfvJI8TlhqvWYEWSgyskBc2lKvGqPUUQk"
DEVELOPER_KEY = "AIzaSyBTRVA_zJ2rx4KIFoGLyfNAoa6jOYRdp0g"
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
            part='id,snippet',
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
            part='snippet',
        ).execute()

        videos = []

        for result in results.get('items', []):
            if result['kind'] == 'youtube#video':
                videos.append(result)

        return results, videos


"""
    def __search(self, options):
        print options

        response = self.api.search().list(
            q=options['q'],
            part="id,snippet",
            maxResults=options['max_results']
        ).execute()

        # import json
        # return json.dumps(response)

        return Response(response)


class Video():
    def __init__(self, object):
        if object:
            snippet = object['snippet']

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


class Item():
    @staticmethod
    def get_item_instance(item):
        if item['id']['kind'] == 'youtube#video':
            return Video(item)


class Response():
    def __init__(self, response):
        if response['kind'] == 'youtube#searchListResponse':
            self.next_page_token = response['nextPageToken']
            self.kind = response['kind']
            self.results_per_page = response['pageInfo']['resultsPerPage']
            self.total_results= response['pageInfo']['totalResults']

            items = []
            for item in response['items']:
                instance = Item.get_item_instance(item)
                if instance:
                    items.append(instance)

            self.items = items

def youtube_search(options):
  youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY
  )

  # Call the search.list method to retrieve results matching the specified query term.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = []
  playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
    elif search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))

  print "Videos:\n", "\n".join(videos), "\n"
  print "Channels:\n", "\n".join(channels), "\n"
  print "Playlists:\n", "\n".join(playlists), "\n"
"""