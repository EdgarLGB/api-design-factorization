#!/usr/bin/env bash

export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=app/app.py
export APP_SETTINGS=../settings.cfg

flask run