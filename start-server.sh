#!/usr/bin/env bash
# start-server.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (python manage.py createsuperuser --no-input --email "admin@need.email" --settings=mensajeria_tei.settings)
fi
(gunicorn --env DJANGO_SETTINGS_MODULE=mensajeria_tei.settings --log-level $GUNICORN_LOG_LEVEL mensajeria_tei.wsgi --user www-data --bind 0.0.0.0:8001 --workers 5) &
nginx -g "daemon off;"
