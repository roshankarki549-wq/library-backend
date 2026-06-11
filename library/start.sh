#!/bin/bash
cd /library

python manage.py migrate
python manage.py collectstatic --noinput

gunicorn --chdir /library.wsgi:application --bind 0.0.0.0:$PORT