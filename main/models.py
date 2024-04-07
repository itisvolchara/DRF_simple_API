from django.db import models
from django.contrib.auth.models import User


class ApiRequest(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    content = models.JSONField('Content')
    date_time = models.DateTimeField('Request time', auto_now_add=True)

    class Meta:
        verbose_name = 'ApiRequest'
        verbose_name_plural = 'ApiRequests'

# Create your models here.
