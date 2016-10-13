from game_data.models import ClassData, RaceData, SpecData
import requests, json
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from django.conf import settings
WOW_KEY = settings.WOW_KEY

class Command(BaseCommand):

    def handle(self, *args, **options):
        ClassData.objects.all().delete()
        data = requests.get("https://us.api.battle.net/wow/data/character/classes?locale=en_US&apikey=%s"%WOW_KEY)
        snapshot = timezone.now()
        j = json.loads(data._content)
        for k in j['classes']:
            newdata = ClassData()
            for kk in k:
                setattr(newdata, str(kk), k[kk])
            newdata.pull_date = snapshot
            newdata.save()

        RaceData.objects.all().delete()
        data = requests.get("https://us.api.battle.net/wow/data/character/races?locale=en_US&apikey=%s"%WOW_KEY)
        snapshot = timezone.now()
        j = json.loads(data._content)
        for k in j['races']:
            newdata = RaceData()
            for kk in k:
                setattr(newdata, str(kk), k[kk])
            newdata.pull_date = snapshot
            newdata.save()

        # SpecData.objects.all().delete()
        # data = requests.get("https://us.api.battle.net/wow/leaderboard/3v3?locale=en_US&apikey=%s"%WOW_KEY)
        # snapshot = timezone.now()
        # j = json.loads(data._content)
        # for k in j['rows']:
        #     newdata = SpecData()
        #     for kk in k:
        #         setattr(newdata, str(kk), k[kk])
        #     newdata.pull_date = snapshot
        #     newdata.save()
