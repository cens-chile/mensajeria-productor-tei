from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class CheckSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=100)

class LogoutSerializer(serializers.Serializer):
    details = serializers.CharField(required=False, allow_blank=True)

class LogoutRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, allow_blank=False)