from django.contrib.auth.models import User, Group

from rest_framework import serializers, viewsets


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Groupfields = ('url', 'name')