#!/usr/bin/env bash

set -o errexit

pipenv run python manage.py migrate

pipenv run gunicorn -b:8000 project.wsgi:application
