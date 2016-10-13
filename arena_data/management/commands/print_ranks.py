from arena_data.models import data_3v3
from game_data.models import ClassData, RaceData
import requests, json
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

class Command(BaseCommand):

    def handle(self, *args, **options):
        print data_3v3.fresh.filter(name="Xaryu").values("pull_date")
        #dd = data_3v3.objects.order_by('ranking')[0:10]
        #for d in dd:
        #    print ClassData.objects.get(pk=d.classId).name, RaceData.objects.get(pk=d.raceId).name
