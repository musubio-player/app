from django.contrib.auth.models import User

from rest_framework import viewsets, serializers

from player.models import Room, Post, RoomPosts
from userprofile.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Post
        fields = ('title', 'youtube_id', 'duration', 'user', 'slug', 'date_published', 'date_updated', 'is_published')

class RoomPostsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    post = PostSerializer()

    class Meta:
        model = RoomPosts
        fields = ('post', 'user', 'order', 'date_added')

class RoomSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    posts = RoomPostsSerializer(many=True)

    class Meta:
        model = Room
        fields = ('id', 'title', 'description', 'user', 'slug', 'posts')
        # depth = 1

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer