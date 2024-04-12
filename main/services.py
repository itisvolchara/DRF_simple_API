from abc import abstractmethod
from datetime import datetime

import requests

from .models import ApiRequest
from .specialclasses import Singleton
from .cache import Cache


class BaseService(Singleton):

    def __init__(self):
        self.cache = Cache()
        self.data = None


class RequestService(BaseService):
    @staticmethod
    @abstractmethod
    def get(*args):
        pass


class CityRequestService(RequestService):

    @staticmethod
    def get(lat, lon):
        city_search = requests.get('https://geocode-maps.yandex.ru/1.x/',
                                   params={'apikey': '///API KEY HERE///',
                                           'geocode': f'{lat},{lon}',
                                           'lang': 'en_US',
                                           'format': 'json',
                                           'kind': 'locality',
                                           'sco': 'latlong'}).json()

        if (city_search['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['results']
                == '0'):
            raise ValueError("There's no cities nearby")

        return city_search


class WeatherRequestService(RequestService):
    def get(self, place, user):
        if self.cache.find(place):
            result = self.cache.get(place)

        else:
            result = requests.get("http://api.weatherapi.com/v1/forecast.json",
                                  params={'q': place,
                                          'key': '///API KEY HERE///'}).json()
            now = datetime.now()
            tomorrow = datetime(now.year, now.month, now.day + 1)
            expires = tomorrow.timestamp() - now.timestamp()
            self.cache.set(place, result, expires)

        ApiRequest(user=user, content=result).save()

        return result
