from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'password', 'is_active', 'is_staff']

    def validate_password(self, value: str) -> str:
        return make_password(value)


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