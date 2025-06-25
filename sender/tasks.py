from __future__ import absolute_import, unicode_literals

import logging
import socket
from django.utils import timezone

import requests
from celery import shared_task
from django.conf import settings
from fhirclient.models.bundle import Bundle
from fhirclient.models.fhirabstractbase import FHIRValidationError
from fhirclient.models.meta import Meta
from fhirclient.models.servicerequest import ServiceRequest
from requests import RequestException
from requests.auth import HTTPBasicAuth
from django.core.cache import cache
from requests.exceptions import InvalidJSONError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.utils import aware_utcnow

from mensajeria_tei.tools import find_resource_in_bundle_by_profile, ProfileList
from sender.models import Mensaje


logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - %(message)s', datefmt='%d/%b/%Y %H:%M:%S')
logger = logging.getLogger(__name__)


@shared_task
def clear_blacklisted():
    OutstandingToken.objects.filter(expires_at__lte=aware_utcnow()).delete()
    BlacklistedToken.objects.filter(blacklisted_at__lte=aware_utcnow()).delete()


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def send_bundle(self, bundle, _id):
    def save_error(mensaje, error):
        mensaje.intento = mensaje.intento + 1
        logger.error("message: %s", error)
        mensaje.mensaje_resultado_error = error
        if mensaje.intento > 6:
            mensaje.estado = 'error'
        else:
            mensaje.estado = 'reintento'
        mensaje.save()
    def get_token(mensaje):
        logger.info("Inicio Autenticación")
        auth_url = settings.TEI_AUTH_SERVER
        auth = HTTPBasicAuth(settings.TOKEN_USER, settings.TOKEN_PASSWORD)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials"
        }
        try:
            auth_r = requests.post(auth_url, data=data, headers=headers, auth=auth)
            if auth_r.status_code != 200:
                return None
            credential = auth_r.json()
        except (RequestException, InvalidJSONError) as e:
            save_error(mensaje, str(e))
            logger.error("raise RequestException")
            raise Exception

        if 'access_token' in credential:
            logger.info("Token Obtenido")
            try:
                cache.set('token', credential['access_token'], int(credential['expires_in']) - 100)
            except ConnectionError:
                # Handle cache connection error
                logger.error("Cache Set Connection Exception")
            logger.info("Fin Autenticación")
            return credential['access_token']
        return None

    mensaje = Mensaje.objects.get(pk=_id)
    token = None
    try:
        token = cache.get('token')
    except ConnectionError as exc:
        # Handle cache connection error
        logger.error("Cache Get Connection Exception")
    except socket.gaierror as exc:
        # Handle other potential connection errors, especially for
        # older Python versions
        logger.error("Cache Get Socket Exception")
    if token:
        logger.info("Using Token from Cache")
    else:
        token = get_token(mensaje)
        if token:
            logger.info("Using new Token")
        else:
            error_message = "No se pudo obtener el Token"
            save_error(mensaje,error_message)
            raise Exception(error_message)
    headers = {
        "Content-Type": "application/json",
        "Authorization": 'Bearer {}'.format(token)
    }
    fhir_url = settings.TEI_FHIR_SERVER
    logger.info("Procesando mensaje id_mensaje: %s", _id)
    #print("bundle: {}", bundle)
    ## Agregar Try except para el registro de los intentos antes de la exception: ConnectionError
    try:
        fhir_r = requests.post(fhir_url, json=bundle, headers=headers)
    except (RequestException, InvalidJSONError) as e:
        save_error(mensaje, str(e))
        raise Exception(str(e))
    if fhir_r.status_code == 200:
        data = fhir_r.json()
        mensaje.mensaje_resultado = data
        if 'resourceType' in data and data['resourceType'] == 'Bundle':
            mensaje.estado = 'enviado'
            mensaje.fecha_recepcion = timezone.now()
            try:
                bundle_resource = Bundle(jsondict=data)
                evento = mensaje.evento
                if evento == 'iniciar':
                    profile_sv = 'https://interoperabilidad.minsal.cl/fhir/ig/tei/StructureDefinition/ServiceRequestLE'
                    service_request_resource = find_resource_in_bundle_by_profile(bundle_resource, profile_sv)
                    if not service_request_resource:
                        logger.info("No se pudo obtener el Id de Interconsulta")
                    else:
                        service_request = ServiceRequest(jsondict=service_request_resource.as_json())
                        id_interconsulta = service_request.identifier[0].value
                        mensaje.id_interconsulta = id_interconsulta
            except (FHIRValidationError, ValueError, Exception) as e:
                logger.error("details: {}".format(str(e)))
            logger.info("Envio correcto mensaje id_mensaje: %s", _id)
            #logger.info("response: %s", fhir_r.json())
        else:
            mensaje.estado = 'error'
        mensaje.save()
    else:
        error_message = "Status: {} - {}".format(fhir_r.status_code, fhir_r.text)
        save_error(mensaje,error_message)
        fhir_r.raise_for_status()

