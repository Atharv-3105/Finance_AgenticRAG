import time 

_cache = {}

def get_cache(key):
    value = _cache.get(key)
    if not value:
        return None
    
    data, expiry = value 
    if time.time() > expiry:
        _cache.pop(key, None)
        return None
    return data


def set_cache(key, value, ttl: int):
    _cache[key] = (value, time.time() + ttl)