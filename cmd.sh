#!/bin/bash
# chmod +x migrations.sh
# ./migrations.sh
python3.8 manage.py makemigrations
python3.8 manage.py migrate
# python3.8 manage.py collectstatic --noinput
# Todo: add outomate superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'password')" | python3.8 manage.py shell 
echo "Server Started..."
python3.8 manage.py runserver 0.0.0.0:8000
echo "khodafez"
