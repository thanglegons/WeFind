import redis

HOST = 'localhost'
PORT = 6379

redis = redis.Redis(host=HOST, port=PORT, db=0)


def set_cache(key, value):
    redis.set(key, value)


def get_cache(key):
    return redis.get(key)
