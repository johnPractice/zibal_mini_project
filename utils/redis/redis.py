import redis
from minizibal.settings import REDIS_HOST, REDIS_PORT
r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def set_value(key, value):
    try:
        r.set(key, value)
        return True
    except Exception as e:
        print(e)
        return False


def get_value(key):
    try:
        value = r.get(key)
        print(value)
        if not value:
            return None
        return value
    except Exception as e:
        print(f' in the redis   {e}')
        return False


def remove_item(key):
    try:
        r.delete(key)
        return True
    except:
        return False
