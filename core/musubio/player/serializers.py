from django.contrib.auth.models import User

from rest_framework import viewsets, serializers

from player.models import Channel, Post, ChannelPosts
from userprofile.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Post
        fields = ('title', 'youtube_id', 'duration', 'user', 'slug', 'date_published', 'date_updated', 'is_published')

class ChannelPostsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    post = PostSerializer()

    class Meta:
        model = ChannelPosts
        fields = ('post', 'user', 'order', 'date_added')

class ChannelSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    posts = ChannelPostsSerializer(many=True)

    class Meta:
        model = Channel
        fields = ('id', 'title', 'description', 'user', 'slug', 'posts')
        # depth = 1

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer