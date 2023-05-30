from django.db import models
from django.conf import settings

class Group(models.Model):
    name=models.CharField(max_length=50)
    desc=models.CharField(max_length=100)
    owner=models.ForeignKey(settings.AUTH_USER_MODEL)
    