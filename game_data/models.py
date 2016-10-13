from __future__ import unicode_literals

from django.db import models

# Create your models here.
# "classes": [{
#         "id": 3,
#         "mask": 4,
#         "powerType": "focus",
#         "name": "Hunter"
#     }, {

class ClassData(models.Model):
    mask = models.IntegerField()
    powerType = models.CharField(max_length=256)
    name = models.CharField(max_length=256)

    pull_date = models.DateTimeField()

# "races": [{
#         "id": 1,
#         "mask": 1,
#         "side": "alliance",
#         "name": "Human"
#     }, {

class RaceData(models.Model):
    mask = models.IntegerField()
    side = models.CharField(max_length=256)
    name = models.CharField(max_length=256)

    pull_date = models.DateTimeField()

class SpecData(models.Model):
    pass
