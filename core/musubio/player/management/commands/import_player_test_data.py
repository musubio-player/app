from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from common.utils import console
from player.models import Room, Post, RoomPosts
from player.management.commands.data.posts import POST_DATA
from player.management.commands.data.rooms import ROOM_DATA


class Command(BaseCommand):
    def handle(self, *args, **options):
        console('Generating test data...')

        # Clear out data.
        Post.objects.all().delete()
        Room.objects.all().delete()

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

        for room_data in ROOM_DATA:
            # Get random user.
            User = get_user_model()
            user = User.objects.filter(id__gt=1).order_by('?')[0]

            order = 1

            # Create the room.
            room = Room()
            room.title = room_data['title']
            room.description = room_data['description']
            room.user = user
            room.save()

            print '[CREATED] room: %s' % (room.title)

            # Add videos to room.
            for youtube_id in room_data['posts']:
                post = Post.objects.get(youtube_id=youtube_id)

                # Add the post to the room.
                room_posts = RoomPosts()
                room_posts.room = room
                room_posts.post = post
                room_posts.order = order
                room_posts.user = user
                room_posts.save()

                print '[ADDED] post to room: %s' % (post.title)

                order = order + 1

            # Add Rick Role to every room.
            room_posts = RoomPosts()
            room_posts.room = room
            room_posts.post = rick_roll
            room_posts.order = order
            room_posts.user = user
            room_posts.save()

            order = order + 1


