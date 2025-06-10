from django.contrib.auth.models import Group, User
from rest_framework import serializers


class MensajeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']