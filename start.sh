#!/bin/bash
cd /library.library

python manage.py migrate
python manage.py collectstatic --noinput

gunicorn --chdir /app/library.wsgi:application --bind 0.0.0.0:$PORT