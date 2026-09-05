import redis

def setup_redis(redis_url):
    if not redis_url:
        return None

    url = redis_url
    if url.startswith("valkey://"):
        url = "redis://" + url[len("valkey://"):]
    elif url.startswith("valkeys://"):
        url = "rediss://" + url[len("valkeys://"):]

    return redis.from_url(url, decode_responses=True)
