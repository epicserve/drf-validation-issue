#!/usr/bin/env bash

GREEN=$(tput -Txterm setaf 2)
GREEN=$(tput -Txterm setaf 2)
YELLOW=$(tput -Txterm setaf 3)
WHITE=$(tput -Txterm setaf 7)
RESET=$(tput -Txterm sgr0)


function ask_yes_or_no_default_no() {
    read response"?${GREEN}$1${RESET} ${WHITE}(y/N)${RESET}${GREEN}?${RESET} "
    if [[ $response =~ ^(no|n| ) ]] || [[ -z $response ]]; then
        echo "no"
    else
        echo "yes"
    fi
}

if test -f "db.sqlite3"; then
    if [[ "yes" = $(ask_yes_or_no_default_no "It looks like you've already loaded the initial data. Do you want remove existing data and start over") ]]; then
        rm db.sqlite3
        rm .env
    else
        echo "Quit. Nothing changed."
        return
    fi
else
    mkvirtualenv drf-validation-issue
    echo `pwd` >  $VIRTUAL_ENV/.project
fi

pip install poetry
poetry install
export SECRET_KEY=$(python -c "import random; print(''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789%^&*(-_=+)') for i in range(50)))")
cat > .env <<EOF
DEBUG=true
SECRET_KEY='$SECRET_KEY'
EOF
./manage.py migrate
./manage.py load_initial_data
