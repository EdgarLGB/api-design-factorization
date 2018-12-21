#!/usr/bin/env bash

export FLASK_APP=factor_app
export FLASK_ENV=development
export WORKER_NUM=4
export REDIS_HOST=172.17.0.2
export REDIS_PORT=6379
export REDIS_MAX_CONN=5

flask run --host=0.0.0.0
