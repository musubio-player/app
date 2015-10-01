from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from common.models import SimpleContentModel, BaseModel

class BaseSocial(BaseModel):
    class Meta:
        abstract = True

    date_created = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

class Comment(BaseSocial, SimpleContentModel):
    body = models.TextField(null=False, blank=False)
    parent_comment = models.ForeignKey('Comment', null=True)

class Follow(BaseSocial):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # user_following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following')