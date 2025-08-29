#!/bin/bash

set -e

CELERY_WORKER_NAME=${CELERY_WORKER_NAME:-""}
CELERY_WORKER_NAME_WITH_UUID=`cat /tmp/celery-worker-$CELERY_WORKER_NAME.tmp`

celery -A ${APP:-""} inspect ping -t 60 -d "celery@$CELERY_WORKER_NAME_WITH_UUID"
