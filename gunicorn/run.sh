#! /bin/bash

python manage.py collectstatic --noinput && 
python manage.py makemigrations && 
python manage.py migrate && 
gunicorn -w 2 -b :8000 kms.wsgi