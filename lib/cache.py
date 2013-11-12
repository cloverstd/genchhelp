# coding: utf-8

import redis
import functools
try:
    import cPickle as pickle
except ImportError:
    import pickle
try:
    import hashlib
    sha1 = hashlib.sha1
except ImportError:
    import sha
    sha1 = sha.new

def _compute_key(function, *args, **kwargs):
    key = pickle.dumps((function.func_name, args, kwargs))
    return sha1(key).hexdigest()

def _prefix(key):
    return "Cache: %s" % key

_redis_cache = redis.StrictRedis()

def CommonCache(expires=86400):
    def _cache(func):
        @functools.wraps(func)
        def wraps(*args, **kwargs):


            key = _compute_key(func, args, kwargs)
            print expires

            if _redis_cache.exists(_prefix(key)):
                return pickle.loads(_redis_cache.get(_prefix(key)))

            result = func(*args, **kwargs)

            pickled = pickle.dumps(result)
            pipe = _redis_cache.pipeline()
            pipe.set(_prefix(key), pickled)
            pipe.expire(_prefix(key), expires)
            pipe.execute()


            return result

        return wraps

    return _cache
