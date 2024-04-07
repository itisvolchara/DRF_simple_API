from django.urls import path, re_path, include
from . import views
from .views import ForecastAPIView, UserRequestsAPIView

urlpatterns = [
    # path('', views.index),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/dailyforecast/', ForecastAPIView.as_view()),
    path('api/v1/userrequests/', UserRequestsAPIView.as_view()),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken'))
]
