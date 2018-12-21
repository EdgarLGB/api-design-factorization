import json

from flask import request

from factor_app import app
from factor_app import factor_service
from factor_app import redis_service


@app.route('/')
def hello():
    return 'Hello Factor factor_app!\n'


@app.route('/factor', methods=['POST'])
def factorization():
    content = request.get_json()
    num = content['number']
    task_id = factor_service.submit(num)
    # initiate the waiting result into redis
    redis_service.update(task_id, 'Calculating...')
    # submit the task and return the task id with status code 202
    res = {'task_id': task_id}
    return json.dumps(res), 202


@app.route('/get/<task_id>')
def get_result(task_id):
    res = redis_service.get(int(task_id))
    if res is None:
        return 'Task_id {} does not exist'.format(task_id), 404
    response = {'result': res.decode("utf-8")}
    return json.dumps(response), 200
