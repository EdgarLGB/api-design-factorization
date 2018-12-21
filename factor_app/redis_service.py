import redis
import os

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
