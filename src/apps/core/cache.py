from django.core.cache import cache
from django.conf import settings

CACHE_TTL = getattr(settings, "CACHE_TTL", 600)
# pega o TTL padrão, caso contrário 10 minutos


def cache_get(key):
    return cache.get(key)


# recebe uma key e retona o valor armazenado no cache


def cache_set(key, value, ttl=CACHE_TTL):
    cache.set(key, value, ttl)


# abstrai o uso do cache


def cache_delete(key):
    cache.delete(key)


# remove o valor do cache
