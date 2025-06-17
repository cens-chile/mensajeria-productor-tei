from __future__ import absolute_import, unicode_literals

import logging
from datetime import timezone, datetime

import requests
from celery import shared_task, Celery
from celery.schedules import crontab
from django.conf import settings
from requests.auth import HTTPBasicAuth
from django.core.cache import cache
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.utils import aware_utcnow
from sender.models import Mensaje

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - %(message)s', datefmt='%d/%b/%Y %H:%M:%S')
logger = logging.getLogger(__name__)


@shared_task
def clear_blacklisted():
    OutstandingToken.objects.filter(expires_at__lte=aware_utcnow()).delete()
    BlacklistedToken.objects.filter(blacklisted_at__lte=aware_utcnow()).delete()


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def send_bundle(self, bundle, _id):
    def get_token():
        logger.info("inicio authenticación")
        auth_url = settings.TEI_AUTH_SERVER
        auth = HTTPBasicAuth(settings.TOKEN_USER, settings.TOKEN_PASSWORD)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials"
        }
        auth_r = requests.post(auth_url, data=data, headers=headers, auth=auth)
        if auth_r.status_code != 200:
            return None
        credential = auth_r.json()

        if 'access_token' in credential:
            logger.info("access_token: %s", credential['access_token'])
            cache.set('token', credential['access_token'], int(credential['expires_in']) - 100)
            logger.info("fin authenticación")
            return credential['access_token']
        return None

    token = cache.get('token')
    if not token:
        token = get_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": 'Bearer {}'.format(token)
    }
    fhir_url = settings.TEI_FHIR_SERVER
    logger.info("token: %s", token)
    logger.info("url: %s", fhir_url)
    logger.info("bundle: %s", bundle)
    logger.info("headers: %s", headers)
    logger.info("_id: %s", _id)
    print("bundle: {}", bundle)
    fhir_r = requests.post(fhir_url, json=bundle, headers=headers)
    mensaje = Mensaje.objects.get(pk=_id)
    if fhir_r.status_code == 200:
        data = fhir_r.json()
        mensaje.mensaje_resultado = fhir_r.json()
        if 'resourceType' in data and data['resourceType'] == 'Bundle':
            mensaje.estado = 'enviado'
            mensaje.fecha_recepcion = datetime.now()
            logger.info("envio correcto: %s", fhir_r.status_code)
            logger.info("response: %s", fhir_r.json())
        else:
            mensaje.estado = 'error'
        mensaje.save()
    else:
        mensaje.intento = mensaje.intento + 1
        mensaje.mensaje_resultado = fhir_r.json()
        logger.error("envio falló: %s", fhir_r.status_code)
        logger.error("response: %s", fhir_r.json())
        if mensaje.intento == 5:
            mensaje.estado = 'error'
        else:
            mensaje.estado = 'reintento'
        mensaje.save()
        raise Exception()

