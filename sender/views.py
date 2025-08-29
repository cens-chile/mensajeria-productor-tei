import logging

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, PolymorphicProxySerializer, OpenApiExample
from fhirclient.models.bundle import Bundle, BundleEntry
from fhirclient.models.fhirabstractbase import FHIRValidationError
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.identifier import Identifier
from fhirclient.models.messageheader import MessageHeader, MessageHeaderSource
from fhirclient.models.meta import Meta
from fhirclient.models.organization import Organization
from fhirclient.models.practitionerrole import PractitionerRole
from fhirclient.models.servicerequest import ServiceRequest
from rest_framework import mixins, generics, permissions, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mensajeria_tei.tools import find_resource_in_bundle_by_profile, find_resource_in_bundle, ProfileList
from users.views import IsAdminOrSender
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
                        'evento', 'estado', 'software', 'organizacion', 'fecha_envio', 'fecha_recepcion')
    search_fields = ('id_interconsulta',
                        'evento', 'estado', 'software', 'organizacion')
    ordering_fields = '__all__'
    ordering = ['fecha_envio']
    permission_classes = [IsAdminOrSender]

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
    permission_classes = [IsAdminOrSender]


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
@permission_classes((IsAdminOrSender,))
def process_message(request):
    bundle = request.data
    try:
        bundle_resource = Bundle(jsondict=bundle)
        meta = Meta(jsondict=bundle_resource.meta.as_json())
        profile = meta.profile[0]
        evento = ProfileList(profile).name
        if 'entry' not in bundle_resource.as_json() or len(bundle_resource.entry) == 0:
            return Response({"details": "Bundle.entry is empty"}, status=status.HTTP_412_PRECONDITION_FAILED)
        bundle_entry = BundleEntry(jsondict=bundle_resource.entry[0].as_json())
        if 'resource' not in bundle_entry.as_json():
            return Response({"details": "Bundle.entry[0] does not have a resource"}, status=status.HTTP_412_PRECONDITION_FAILED)
        message_header = MessageHeader(jsondict=bundle_entry.resource.as_json())
        if 'source' not in message_header.as_json():
            return Response({"details": "MessageHeader does not have a source"}, status=status.HTTP_412_PRECONDITION_FAILED)
        source = MessageHeaderSource(jsondict=message_header.source.as_json())
        if 'software' not in source.as_json():
            return Response({"details": "MessageHeader.source does not have a software"},
                            status=status.HTTP_412_PRECONDITION_FAILED)
        software = source.software
        if 'author' not in message_header.as_json():
            return Response({"details": "MessageHeader does not have a author"},
                            status=status.HTTP_412_PRECONDITION_FAILED)
        fhir_reference = FHIRReference(jsondict=message_header.author.as_json())
        if 'reference' not in fhir_reference.as_json():
            return Response({"details": "MessageHeader.author does not have a reference"},
                            status=status.HTTP_412_PRECONDITION_FAILED)
        practitioner_role_reference = fhir_reference.reference
        practitioner_role_resource = find_resource_in_bundle(bundle_resource, practitioner_role_reference)
        if not practitioner_role_resource:
            return Response({"details": "MessageHeader.author.reference {} does not have a match resource in bundle".format(practitioner_role_reference)},
                            status=status.HTTP_412_PRECONDITION_FAILED)
        practitioner_role = PractitionerRole(jsondict=practitioner_role_resource.as_json())
        if 'organization' not in practitioner_role.as_json():
            return Response({"details": "PractitionerRole does not have a organization"},
                            status=status.HTTP_412_PRECONDITION_FAILED)
        fhir_reference = FHIRReference(jsondict=practitioner_role.organization.as_json())
        if 'reference' not in fhir_reference.as_json():
            return Response({"details": "PractitionerRole.organization does not have a reference"},
                            status=status.HTTP_412_PRECONDITION_FAILED)
        organization_reference = fhir_reference.reference
        organization_resource = find_resource_in_bundle(bundle_resource, organization_reference)
        if not organization_resource:
            return Response({"details": "PractitionerRole.organization.reference {} does not have a match resource in bundle".format(
                organization_reference)},
                            status=status.HTTP_412_PRECONDITION_FAILED)
        organization = Organization(jsondict=organization_resource.as_json())
        if 'name' not in organization.as_json():
            return Response({"details": "Organization does not have a name"},
                            status=status.HTTP_412_PRECONDITION_FAILED)
        organization_name = organization.name
    except (FHIRValidationError, ValueError, Exception) as e:
        return Response({"details": "{}".format(str(e))}, status=status.HTTP_412_PRECONDITION_FAILED)
    if evento != 'iniciar':
        profile_sv = 'https://interoperabilidad.minsal.cl/fhir/ig/tei/StructureDefinition/ServiceRequestLE'
        service_request_resource = find_resource_in_bundle_by_profile(bundle_resource, profile_sv)
        if not service_request_resource:
            return Response({"details": "{} does not match resource in bundle".format(
                profile_sv)},
                            status=status.HTTP_412_PRECONDITION_FAILED)
        service_request = ServiceRequest(jsondict=service_request_resource.as_json())
        if 'identifier' not in service_request.as_json()  or len(service_request.identifier) == 0:
            return Response({"details": "ServiceRequest does not have an identifier"},
                            status=status.HTTP_412_PRECONDITION_FAILED)
        identifier_entry = Identifier(jsondict=service_request.identifier[0].as_json())
        if 'value' not in identifier_entry.as_json():
            return Response({"details": "ServiceRequest.identifier[0] does not have a value"},
                            status=status.HTTP_412_PRECONDITION_FAILED)
        id_interconsulta = identifier_entry.value
        mensaje = Mensaje(id_interconsulta=id_interconsulta, evento=evento, software=software, organizacion=organization_name)
    else:
        mensaje = Mensaje(evento=evento, software=software, organizacion=organization_name)
    mensaje.save()
    _id = mensaje.id_mensaje
    #logging.info("bundle: %s", bundle)
    send_bundle.apply_async(args=(bundle, _id))
    #send_bundle(bundle, _id)
    headers = {
        "Location": "/mensaje/{}".format(_id)
    }
    return Response({"details": "Mensaje Recibido", "location": "/mensaje/{}".format(_id)},
                    status=status.HTTP_200_OK,
                    headers=headers)

