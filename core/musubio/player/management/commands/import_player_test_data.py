from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from common.utils import console
from player.models import Channel, Post, ChannelPosts
from player.management.commands.data.posts import POST_DATA
from player.management.commands.data.channels import CHANNEL_DATA


class Command(BaseCommand):
    def handle(self, *args, **options):
        console('Generating test data...')

        # Clear out data.
        Post.objects.all().delete()
        Channel.objects.all().delete()

        # Import posts.
        for post_data in POST_DATA:
            # Get random user.
            User = get_user_model()
            user = User.objects.filter(id__gt=1).order_by('?')[0]

            post = Post()
            post.title = post_data['title']
            post.youtube_id = post_data['youtube_id']
            post.duration = post_data['duration']
            post.user = user
            post.save()

            print '[CREATED] post: %s' % (post.title)

        rick_roll = Post.objects.get(youtube_id='dQw4w9WgXcQ')

        for channel_data in CHANNEL_DATA:
            # Get random user.
            User = get_user_model()
            user = User.objects.filter(id__gt=1).order_by('?')[0]

            order = 1

            # Create the channel.
            channel = Channel()
            channel.title = channel_data['title']
            channel.description = channel_data['description']
            channel.user = user
            channel.save()

            print '[CREATED] channel: %s' % (channel.title)

            # Add videos to channel.
            for youtube_id in channel_data['posts']:
                post = Post.objects.get(youtube_id=youtube_id)

                # Add the post to the channel.
                channel_posts = ChannelPosts()
                channel_posts.channel = channel
                channel_posts.post = post
                channel_posts.order = order
                channel_posts.user = user
                channel_posts.save()

                print '[ADDED] post to channel: %s' % (post.title)

                order = order + 1

            # Add Rick Role to every channel.
            channel_posts = ChannelPosts()
            channel_posts.channel = channel
            channel_posts.post = rick_roll
            channel_posts.order = order
            channel_posts.user = user
            channel_posts.save()

            order = order + 1


