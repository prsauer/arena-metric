from arena_data.models import data_3v3
import requests, json
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from django.conf import settings
WOW_KEY = settings.WOW_KEY

class Command(BaseCommand):

    def handle(self, *args, **options):
        #data_3v3.objects.all().delete()
        data = requests.get("https://us.api.battle.net/wow/leaderboard/3v3?locale=en_US&apikey=%s"%WOW_KEY)
        snapshot = timezone.now()
        #print data
        #import pdb; pdb.set_trace()
        j = json.loads(data._content)
        for k in j['rows']:
            newdata = data_3v3()
            for kk in k:
                setattr(newdata, str(kk), k[kk])
            newdata.pull_date = snapshot
            newdata.save()
