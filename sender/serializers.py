from django.contrib.auth.models import Group, User
from rest_framework import serializers

from sender.models import Mensaje


class MensajeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mensaje
        fields = ['id_mensaje', 'id_interconsulta', 'evento', 'estado', 'organizacion', 'fecha_envio', 'intento', 'fecha_recepcion', 'mensaje_resultado']
