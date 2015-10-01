from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

from userprofile.serializers import UserViewSet
from player.serializers import ChannelViewSet, PostViewSet


admin.autodiscover()

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'channels', ChannelViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = patterns('',
    url(
        regex=r'^admin/',
        view=include(admin.site.urls),
    ),
    url(
        regex=r'^api/',
        view=include(router.urls),
    ),
    url(
        regex=r'^api-auth/',
        view=include('rest_framework.urls', namespace='rest_framework'),
    ),
)
