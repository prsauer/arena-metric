from __future__ import unicode_literals

from django.db import models

class ClassData(models.Model):
    mask = models.IntegerField()
    powerType = models.CharField(max_length=256)
    name = models.CharField(max_length=256)

    pull_date = models.DateTimeField()

class RaceData(models.Model):
    mask = models.IntegerField()
    side = models.CharField(max_length=256)
    name = models.CharField(max_length=256)

    pull_date = models.DateTimeField()

class SpecData(models.Model):
    pass
