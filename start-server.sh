#!/usr/bin/env bash
# start-server.sh
echo "Hello from Projet The Toll Registers of Aschach (1706-1740): Database and Analysis"
python manage.py collectstatic --no-input
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (echo "creating superuser ${DJANGO_SUPERUSER_USERNAME}" && python manage.py createsuperuser --no-input --noinput --email 'blank@email.com')
fi
gunicorn djangobaseproject.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3 & nginx -g "daemon off;"