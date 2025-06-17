import logging

from django.contrib.sessions.serializers import JSONSerializer
from django.core.serializers import serialize
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, PolymorphicProxySerializer, OpenApiExample
from rest_framework import mixins, generics, permissions, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mensajeria_tei.wsgi import application
from .models import Mensaje
from .tasks import send_bundle
from .serializers import MensajeSerializer


logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - %(message)s', datefmt='%d/%b/%Y %H:%M:%S')
logger = logging.getLogger(__name__)

class MensajeList(generics.ListAPIView):
    """
        Buscar query
        ordenar asc desc query
        paginar page query
        listar
    """
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ('id_interconsulta',
                        'evento', 'estado', 'organizacion', 'fecha_envio', 'fecha_recepcion')
    search_fields = ('id_interconsulta',
                        'evento', 'estado', 'organizacion')
    ordering_fields = '__all__'
    ordering = ['fecha_envio']
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class MensajeItem(generics.RetrieveAPIView):
    """
        Buscar query
        ordenar asc desc query
        paginar page query
        listar
    """
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(
    request=dict,
    responses=OpenApiTypes.OBJECT,
    examples=[
        OpenApiExample(
            'Bundle',
            {'resourceType': 'Bundle'},
            request_only=True,
            media_type='application/json')]
)
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def process_message(request):
    bundle = request.data
    # Obtener del bundle el ID interconsulta, el evento y la Organización
    evento = "iniciar"
    organizacion = "Mi Organización"
    if evento is not 'iniciar':
        id_interconsulta = "asd"
        mensaje = Mensaje(id_interconsulta=id_interconsulta, evento=evento, organizacion=organizacion)
    else:
        mensaje = Mensaje(evento=evento, organizacion=organizacion)
    mensaje.save()
    _id=mensaje.id_mensaje
    logging.info("bundle: %s", bundle)
    send_bundle.apply_async(args=(bundle, _id))
    return Response({"details": "Mensaje Recibido", "location": "/mensaje/{}".format(_id)}, status=status.HTTP_200_OK)


