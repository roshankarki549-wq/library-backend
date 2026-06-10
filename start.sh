#!/bin/bash

python manage.py migrate
python manage.py collectstatic --noinput

gunicorn library.library.wsgi:application --bind 0.0.0.0:$PORT