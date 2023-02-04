#!/bin/bash

python3 manage.py migrate

uwsgi --ini uwsgi.ini