from django.core.cache import cache

from .specialclasses import Singleton


class Cache(Singleton):

    @staticmethod
    def find(cache_key):
        return cache.has_key(cache_key)
    @staticmethod
    def get(cache_key):
        return cache.get(cache_key)

    @staticmethod
    def set(cache_key, value, expires=1000):
        cache.set(cache_key, value, expires)

    @staticmethod
    def delete(cache_key):
        cache.delete(cache_key)

    @staticmethod
    def clear():
        cache.clear()

