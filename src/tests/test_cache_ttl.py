from django.core.cache import cache
from django.conf import settings

def test_cache_ttl():
    cache.set("test_key", "abc", timeout=settings.CACHE_TTL)
    ttl = cache.ttl("test_key")

    assert ttl <= settings.CACHE_TTL
    assert ttl > settings.CACHE_TTL - 5