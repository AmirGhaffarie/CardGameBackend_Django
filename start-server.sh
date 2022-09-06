#!/usr/bin/env bash
# start-server.sh
python CardGameDB/manage.py makemigrations
python CardGameDB/manage.py migrate
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd CardGameDB; python manage.py createsuperuser --no-input)
fi
(cd CardGameDB; gunicorn CardGameTestDB.wsgi --user www-data --bind 0.0.0.0:8010 --workers 5) &
nginx -g "daemon off;"