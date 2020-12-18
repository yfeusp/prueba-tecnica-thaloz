#!/bin/bash
python ./user_api/manage.py migrate
python ./user_api/manage.py runserver 0.0.0.0:8000
