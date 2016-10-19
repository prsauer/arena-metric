from __future__ import unicode_literals

from django.db import models

from game_data.models import ClassData, RaceData

class PullDataManager(models.Manager):
    def filter(self, *args, **kwargs):
        latest_date = self.order_by('pull_date').last()
        if latest_date:
            latest_date = latest_date.pull_date
        else:
            return self.none()
        return super(PullDataManager, self).filter(pull_date=latest_date, *args, **kwargs)

class PullDataModel(models.Model):
    pull_date = models.DateTimeField()

# Create your models here.
class data_3v3(PullDataModel):
    fresh = PullDataManager()
    ranking = models.IntegerField()
    rating = models.IntegerField()
    name = models.CharField(max_length=256)
    realmId = models.IntegerField()
    realmName = models.CharField(max_length=256)
    realmSlug = models.CharField(max_length=256)
    raceId = models.IntegerField()
    classId = models.IntegerField()
    specId = models.IntegerField()
    factionId = models.IntegerField()
    genderId = models.IntegerField()
    seasonWins = models.IntegerField()
    seasonLosses = models.IntegerField()
    weeklyWins = models.IntegerField()
    weeklyLosses = models.IntegerField()

    dec_race = models.CharField(max_length=256, null=True, default=None)
    dec_class = models.CharField(max_length=256, null=True, default=None)

    def toDict(self):
        return {"id": self.id,
                "ranking": self.ranking,
                "rating": self.rating,
                "class": ClassData.objects.get(pk=self.classId).name,
                "race": RaceData.objects.get(pk=self.raceId).name,
                "name": self.name,
                   }

    def __str__(self):
        if self.dec_race is None:
            self.dec_race = RaceData.objects.get(pk=self.raceId).name
            self.dec_class = ClassData.objects.get(pk=self.classId).name
            self.save()
        return self.name + " <" + self.dec_race + " " + self.dec_class + "> Rank " + str(self.ranking)

from django.contrib import admin

admin.site.register(data_3v3)
