from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, generics, permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Mensaje
from .serializers import MensajeSerializer


class EnviadorDetail(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
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

    def post(self, request, *args, **kwargs):

        return self.create(request, *args, **kwargs)