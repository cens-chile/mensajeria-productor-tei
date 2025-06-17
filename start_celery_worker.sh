#!/bin/bash

set -e

./wait_for_it.sh ${RABBITMQ_HOST}:15672 -t 0
./wait_for_it.sh ${MEMCACHED_SERVER}:11211 -t 0

UUID=$(cat /proc/sys/kernel/random/uuid)
CELERY_WORKER_NAME=${CELERY_WORKER_NAME:-""}
CELERY_WORKER_NAME_WITH_UUID="${CELERY_WORKER_NAME}-${UUID}"

echo "$CELERY_WORKER_NAME_WITH_UUID" > "/tmp/celery-worker-$CELERY_WORKER_NAME.tmp"

celery -A mensajeria_tei worker -n $CELERY_WORKER_NAME_WITH_UUID --loglevel=INFO "$@"