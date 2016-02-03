import endpoints
from protorpc import message_types
from protorpc import remote
from api import api_root

from messages.video import VideoInsertRequest, Video, VideoList
from models.video import VideoModel

package = 'Musubio'


@api_root.api_class(resource_name='musubio')
class VideoApi(remote.Service):
    """Musubi Video API v1"""
    @endpoints.method(message_types.VoidMessage,
                      VideoList,
                      path='videos',
                      http_method='GET',
                      name='video.list')
    def video_list(self, request):
        query = VideoModel.get_list()
        videos = [video.to_message() for video in query.fetch()]

        videoList = VideoList()
        videoList.videos = videos

        return videoList

    @endpoints.method(VideoInsertRequest,
                      Video,
                      path='videos',
                      http_method='POST',
                      name='videos.insert')
    def video_insert(self, request):
        entity = VideoModel.put_from_message(request)
        return entity.to_message()