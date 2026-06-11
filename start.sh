#!/bin/bash
cd/library.library

python manage.py migrate
python manage.py collectstatic --noinput

gunicorn library.wsgi:application --bind 0.0.0.0:$PORT