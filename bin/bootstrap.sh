#!/usr/bin/env bash

mkvirtualenv drf-validation-issue
echo `pwd` >  $VIRTUAL_ENV/.project
pip install poetry
poetry install
export SECRET_KEY=$(python -c "import random; print(''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789%^&*(-_=+)') for i in range(50)))")
cat > .env <<EOF
DEBUG=true
SECRET_KEY='$SECRET_KEY'
EOF
./manage.py migrate
./manage.py load_toppings
./manage.py createsuperuser
