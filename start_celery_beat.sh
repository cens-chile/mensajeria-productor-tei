#!/bin/bash

set -e

./wait_for_it.sh ${RABBITMQ_HOST}:15672 -t 0

celery -A mensajeria_tei beat --loglevel=INFO -s /code/celerybeat-schedule