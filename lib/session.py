# coding: utf-8


import os, time, base64
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


def _generate_session_id(backend):
    """Generate a random id for session"""

    while True:
        rand = os.urandom(16)
        now = time.time()
        secret_key = backend.options["secret_key"]
        session_id = sha1("%s%s%s" %(rand, now, secret_key))
        session_id = session_id.hexdigest()
        if not backend.exists(session_id):
            break

    return session_id

class SessionBackend(object):
    """
    The base Session Backend class
    """

    def getitem(self, key):
        pass

    def setitem(self, key, value, timeout):
        pass

    def delitem(self, key):
        pass

    def exists(self, key):
        pass

    def encode(self, session_dict):
        """encodes session dict as a string"""
        pickled = pickle.dumps(session_dict)
        return base64.encodestring(pickled)

    def decode(self, session_data):
        """decodes the data to get back the session dict """
        pickled = base64.decodestring(session_data)
        return pickle.loads(pickled)

class RedisSessionBackend(SessionBackend):

    def __init__(self, redis_connection, **options):
        self.options = dict(prefix="Session ID:",
                            timeout=86400,
                            #cookie_name="session_id",
                            #cookie_domain=None,
                            #cookie_path=None,
                            secret_key="",
                            )

        self.options.update(options)

        self.redis = redis_connection

    def getitem(self, key):
        if self.exists(key):
            pickled = self.redis.get(self.prefix(key))
            return self.decode(pickled)
        else:
            #raise KeyError, key
            return None

    def setitem(self, key, value, timeout=None):
        """Default timeout: 24 * 60 * 60 seconds"""
        pickled = self.encode(value)
        self.redis.set(self.prefix(key), pickled)
        if timeout:
            self.redis.expire(self.prefix(key), timeout)
        else:
            self.redis.expire(self.prefix(key), self.options["timeout"])

    def delitem(self, key):

        self.redis.delete(self.prefix(key))

    def exists(self, key):

        return bool(self.redis.exists(self.prefix(key)))

    def prefix(self, key):
        return "%s%s" % (self.options["prefix"], key)


class SessionData(dict):

    def __init__(self, session_id=None):
        self.id = session_id
        self.permanent = False
        self.death = False

    def __getitem__(self, key):
        if self.has_key(key):
            return dict.__getitem__(self, key)
        return None

    def kill(self):
        self.death = True

    def __setitem__(self, key, value):
        return dict.__setitem__(self, key, value)

    #def __setattr__(self, key, value):
        #self[key] = value

    #def __getattr__(self, key):
        #return self[key]

    #def __delattr__(self, key):
        #del self[key]


def Session(request):

    import functools
    @functools.wraps(request)
    def Process(handler, *args):
        session_id = handler.get_secure_cookie("session_id")

        item = handler.application.session_backend.getitem(session_id)

        data = None


        if item:
            data = SessionData(item.id)
            data.update(item)
        else:
            data = SessionData()
            handler.clear_cookie("session_id")

        handler.__setattr__("session", data)

        # excute request
        result = request(handler, *args)

        if data.id:
            if data.death:
                handler.clear_cookie("session_id")
                handler.application.session_backend.delitem(data.id)

            elif data["permanent"] == True:
                handler.set_secure_cookie("session_id", data.id)
                handler.application.session_backend.setitem(data.id, data, timeout=86400*31)
            else:
                handler.set_secure_cookie("session_id", data.id, expires_days=None)
                handler.application.session_backend.setitem(data.id, data)

        else:
            if len(data.keys()):
                data.id = _generate_session_id(handler.application.session_backend)
                if data["permanent"] == True:
                    handler.set_secure_cookie("session_id", data.id)
                    handler.application.session_backend.setitem(data.id, data, timeout=86400*31)
                else:
                    handler.set_secure_cookie("session_id", data.id, expires_days=None)
                    handler.application.session_backend.setitem(data.id, data)

        return result

    return Process
