#!/bin/sh

set -o errexit
set -o pipefail

while ! nc -w 1 -z $DATABASE_HOST $DATABASE_PORT; do 
    sleep 0.1
done

python manage.py migrate
python manage.py runserver $HOST:$PORT
