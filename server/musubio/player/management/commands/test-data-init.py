from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from common.utils import console
from player.models import Room, Post, RoomPosts

class Command(BaseCommand):
    def handle(self, *args, **options):
        console('Generating test data...')

        # Clear out data.
        RoomPosts.objects.all().delete()
        Room.objects.all().delete()
        Post.objects.all().delete()

        """
        {
            'youtube_id': '',
            'title': '',
        },
        """

        ROOM_DATA = [
            {
                'title': 'Careless Whispers 24/7',
                'description': 'CW all the time.',
                'user_id': 1,
                'posts': [
                    {
                        'youtube_id': 'izGwDsrQ1eQ',
                        'title': 'George Michael - Careless Whisper (Official Video)',
                        'user_id': 1,
                    },
                    {
                        'youtube_id': 'lVXziMFEqX0',
                        'title': 'Careless Whisper - Vintage 1930\'s Jazz Wham! Cover ft. Dave Koz',
                        'user_id': 1,
                    },
                    {
                        'youtube_id': 'GaoLU6zKaws',
                        'title': 'Sexy Sax Man Careless Whisper Prank feat. Sergio Flores (directors cut)',
                        'user_id': 1,
                    },
                ],
            },
            {
                'title': 'Studying Music',
                'description': 'Keep the brain going.',
                'user_id': 1,
                'posts': [
                    {
                        'youtube_id': 'BJamJGtUh-Q',
                        'title': 'Study Music Project - Caramel Macchiato (Study Music with Alpha Waves)',
                        'user_id': 1,
                    },
                    {
                        'youtube_id': 'M5Hk6Q_jNWg',
                        'title': 'Study Music Project - Reminiscence (Coffee Version)',
                        'user_id': 1,
                    },
                    {
                        'youtube_id': 'iGEQu6cS-rc',
                        'title': 'Study Music Project - Rainy Nights, Rainy Days (Music for Studying)',
                        'user_id': 1,
                    },
                ],
            },
            {
                'title': 'SF Giants TV',
                'description': 'All Giants, all the time.',
                'user_id': 1,
                'posts': [
                    {
                        'youtube_id': 'ucANLv3Z47Y',
                        'title': 'San Francisco Giants Road to the World Series 2014',
                        'user_id': 1,
                    },
                    {
                        'youtube_id': 'BKPLmY-6W9I',
                        'title': 'Buster Olney World Series Recap',
                        'user_id': 1,
                    },
                    {
                        'youtube_id': 'rvAGBcNlCJU',
                        'title': 'Dynasty Cemented: Francisco Giants 2014 Playoffs Highlights',
                        'user_id': 1,
                    },
                ],
            },
        ]

        # Create Rick Roll for testing.
        rr = Post()
        rr.title = 'Rick Astley - Never Gonna Give You Up'
        rr.youtube_id = 'dQw4w9WgXcQ'
        rr.user_id = 1
        rr.save()

        for room_data in ROOM_DATA:
            order = 1

            # Create the room.
            room = Room()
            room.title = room_data['title']
            room.description = room_data['description']
            room.user_id = room_data['user_id']
            room.save()

            # Add videos to room.
            for post_data in room_data['posts']:
                post = Post()
                post.youtube_id = post_data['youtube_id']
                post.title = post_data['title']
                post.user_id = post_data['user_id']
                post.save()

                # Add the post to the room.
                room_posts = RoomPosts()
                room_posts.room = room
                room_posts.post = post
                room_posts.order = order
                room_posts.user_id = 1
                room_posts.save()

                order = order + 1

            # Add Rick Role to every room.
            room_posts = RoomPosts()
            room_posts.room = room
            room_posts.post = rr
            room_posts.order = order
            room_posts.user_id = 1
            room_posts.save()

            order = order + 1


