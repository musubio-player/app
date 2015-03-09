from django.db import models
from django.contrib.auth.models import User

from common.models import BaseModel, ContentModel


class Room(ContentModel):
    description = models.TextField(null=True, blank=True)
    is_private = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def get_posts(self):
        posts = []
        for room_post in self.roomposts_set.all():
            posts.append(room_post.post)

        return posts

class Post(ContentModel):
    youtube_id = models.CharField(max_length=255)

class RoomPosts(models.Model):
    class Meta:
        db_table = 'player_room_posts'

    room = models.ForeignKey(Room, related_name='posts')
    post = models.ForeignKey(Post, related_name='room_posts')
    order = models.IntegerField()
    user = models.ForeignKey(User)
    date_added = models.DateTimeField(auto_now=True)