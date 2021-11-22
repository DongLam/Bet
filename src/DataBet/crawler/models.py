from django.db import models
from django_mongodb_engine.contrib import MongoDBManager
# Create your models here.
from django.utils.datetime_safe import datetime


class Match(models.Model):
    objects = MongoDBManager()
    team1 = models.CharField(max_length=50)
    team2 = models.CharField(max_length=50)
    odds1 = models.DecimalField(max_digits=10, decimal_places=5)
    odds2 = models.DecimalField(max_digits=10, decimal_places=5)
    dateTimeStamp = models.DateTimeField(default=datetime.now, blank=True)
    site = models.CharField(max_length=50, blank=True)
    game = models.CharField(max_length=50, blank=True)