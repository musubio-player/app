from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes import generic

from common.models import BaseModel
# from social.models import Follow


class Profile(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='profile')
    title = models.CharField(max_length=255, null=False, blank=False)
    follows = generic.GenericRelation(settings.AUTH_USER_MODEL)