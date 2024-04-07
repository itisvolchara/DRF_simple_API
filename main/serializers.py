from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .models import ApiRequest

class ApiRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiRequest
        fields = ['content', 'date_time']
