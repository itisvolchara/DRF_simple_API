from django.shortcuts import render
from django.http.response import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
import requests
import re
from .models import ApiRequest
from .serializers import ApiRequestSerializer

from django.core.cache import cache
from django.utils import timezone
from datetime import datetime

# Create your views here.
# def index(request):
#     return HttpResponse('<h1>Test response</h1>')

class UserRequestsAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ApiRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return ApiRequest.objects.filter(user=user)


class ForecastAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        print(request.user)
        print(request.auth)

        latlon = re.findall(r'-?\d+\.?\d*', request.data['latlon'])

        try:
            lat, lon = latlon
        except ValueError:
            return Response({'error': 'Missing latlon data or incorrect latlon format'})

        city_search = requests.get('https://geocode-maps.yandex.ru/1.x/',
                                   params={'apikey': '///API KEY HERE///',
                                           'geocode': f'{lat},{lon}',
                                           'lang': 'en_US',
                                           'format': 'json',
                                           'kind': 'locality',
                                           'sco': 'latlong'}).json()

        if city_search['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData'][
            'results'] == '0':
            return Response({'status': 'error', 'message': "There's no cities nearby"})

        place = city_search['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
            'GeocoderMetaData']['text']

        # print(place)
        if cache.has_key(place):
            res = cache.get(place)
            # print('got that answer from the cache')
        else:
            res = requests.get("http://api.weatherapi.com/v1/forecast.json",
                               params={'q': place,
                                       'key': '///API KEY HERE///'}).json()
            now = datetime.now()
            tomorrow = datetime(now.year, now.month, now.day + 1)
            expires = tomorrow.timestamp() - now.timestamp()
            cache.set(place, res, expires)

        # print(res)

        ApiRequest(user=request.user, content=res).save()

        return Response({'result': res['forecast']['forecastday'][0]})
