from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

import re

from .models import ApiRequest
from .serializers import ApiRequestSerializer
from .services import *

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

    @staticmethod
    def get(request):

        latlon = re.findall(r'-?\d+\.?\d*', request.data['latlon'])

        try:
            lat, lon = latlon
        except ValueError:
            return Response({'error': 'Missing latlon data or incorrect latlon format'})

        try:
            city_search_service = CityRequestService()
            place = city_search_service.get(lat, lon)['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
        except ValueError:
            return Response({'status': 'error', 'message': "There's no cities nearby"})

        weather_search_service = WeatherRequestService()
        result = weather_search_service.get(place, request.user)

        return Response({'result': result['forecast']['forecastday'][0]})
