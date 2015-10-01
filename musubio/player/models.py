from django.db import models
from django.contrib.auth.models import User

from common.models import BaseModel, ContentModel


class Channel(ContentModel):
    description = models.TextField(null=True, blank=True)
    is_private = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def get_posts(self):
        posts = []
        for channel_post in self.channelposts_set.all():
            posts.append(channel_post.post)

        return posts

class Post(ContentModel):
    youtube_id = models.CharField(max_length=255)
    duration = models.IntegerField()

class ChannelPosts(models.Model):
    class Meta:
        db_table = 'player_channel_posts'

    channel = models.ForeignKey(Channel, related_name='posts')
    post = models.ForeignKey(Post, related_name='channel_posts')
    order = models.IntegerField()
    user = models.ForeignKey(User)
    date_added = models.DateTimeField(auto_now=True)