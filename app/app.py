import concurrent.futures
import json
import queue
import random
import os

import redis
from flask import Flask
from flask import request

app = Flask(__name__)


# ----------------------routes-----------------------------
@app.route('/')
def hello():
    return 'Hello Factor app!\n'


@app.route('/factor', methods=['POST'])
def factorization():
    content = request.get_json()
    num = content['number']
    task_id = submit(num)
    # initiate the waiting result into redis
    update(task_id, 'Calculating...')
    # submit the task and return the task id with status code 202
    res = {'task_id': task_id}
    return json.dumps(res), 202


@app.route('/get/<task_id>')
def get_result(task_id):
    res = get(int(task_id))
    if res is None:
        return 'Task_id {} does not exist'.format(task_id), 404
    response = {'result': res.decode("utf-8")}
    return json.dumps(response), 200


# --------------------------------------------------------------

# ----------------------Factorization service--------------------

q = queue.Queue()
executor = concurrent.futures.ThreadPoolExecutor(max_workers=int(os.environ.get("WORKER_NUM")))
service_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)


class FactorizationTask:
    num = None
    id = None

    def __init__(self, num):
        self.num = num
        self.id = random.randint(0, 1000000000)


def __del__():
    executor.shutdown()
    service_executor.shutdown()


def submit(num):
    """
    Submit a task of factorizing the given number
    :param num: a given integer
    :return: task id with which you can look up the status of task
    """
    task = FactorizationTask(num)
    q.put(task)
    return task.id


def fetch():
    return q.get()


def do_factorization(task):
    print("Task {} with number {} kicked off".format(task.id, task.num))
    res = factors(task.num)
    print("Update result {} for task {}".format(res, task.id))
    update(task.id, ','.join(str(e) for e in res))


def run():
    while True:
        task = fetch()
        executor.submit(do_factorization, task)


service_executor.submit(run)

# ---------------------------------------------------

# ------------------------Redis service------------------------------------
redis_pool = redis.ConnectionPool(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"), db=0,
                                  max_connections=int(os.environ.get("REDIS_MAX_CONN")))


def get_connection():
    try:
        conn = redis.Redis(connection_pool=redis_pool)
        print(conn)
        conn.ping()
        print('Connected!')
    except Exception as ex:
        print('Error:', ex)
        exit('Failed to connect, terminating.')
    return conn


def get(name):
    return get_connection().get(name)


def update(name, value):
    get_connection().set(name=name, value=value)


# -----------------------------------------------------------

# -----------------------------Factorization helper-----------------------------
# Returns true if n is a prime number
def check_prime(n):
    x = 2
    while x < n:
        if n % x == 0:
            # Factor other then 1 or n, number is composite
            return False
        x = x + 1
    # Number is prime, while loop terminated without finding factor
    return True


# Finds the next prime after n
def next_prime(n):
    val = n + 1
    while True:
        # Check if val (n + 1) is a prime
        if check_prime(val):
            return val
        else:
            val = val + 1


# Returns prime factors of n. Returns an empty list if n is prime.
def factors(n):
    factor_list = []
    prime = 1
    while next_prime(prime) <= n:
        while n % next_prime(prime) == 0:
            n = n / next_prime(prime)
            factor_list.append(next_prime(prime))
        prime = next_prime(prime)
    return factor_list


if __name__ == '__main__':
    app.run(host="0.0.0.0")
