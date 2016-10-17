from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from arena_data.models import data_3v3
from game_data.models import ClassData, RaceData
import math

def ztest(y1,y2,n1,n2):
    p1 = 1.0*y1/n1
    p2 = 1.0*y2/n2
    P=1.0*(y1+y2)/(n1+n2)
    return (p1 - p2)/math.sqrt( P*(1-P)*( (1.0/n1) + (1.0/n2) )   )

# Create your views here.
def main(request):
    klob = {}
    for k in request.GET.keys():
        klob[k] = request.GET.get(k)

    dd = data_3v3.objects.filter(**klob).order_by('ranking')[0:25]
    print dd.last().__dict__
    j = list()
    #j['data'] = list()
    for d in dd:
        j.append ({"id": d.id, "ranking": d.ranking, "rating": d.rating, "class": ClassData.objects.get(pk=d.classId).name, "race": RaceData.objects.get(pk=d.raceId).name})
    return JsonResponse(j, safe=False)

def stats(request):
    klob = {}
    for k in request.GET.keys():
        klob[k] = request.GET.get(k)

    k = data_3v3.objects.order_by('pull_date').distinct('pull_date').values_list('pull_date', flat=True)

    if settings.DEVEL:
        #sqllite doesnt support .distinct!
        k = data_3v3.objects.first().pull_date,

    dd = {}
    for pull_date in k:
        j = {}
        top_N = int(request.GET.get('top'))
        for c in ClassData.objects.all():
            top_p = data_3v3.objects.filter(pull_date=pull_date, ranking__lt=top_N, classId=c.id)
            top_p = top_p.count()
            top_pop = data_3v3.objects.filter(pull_date=pull_date, ranking__lt=top_N).count()

            low_p = data_3v3.objects.filter(pull_date=pull_date, ranking__gt=2500, classId=c.id)
            low_p = low_p.count()
            low_pop = data_3v3.objects.filter(pull_date=pull_date, ranking__gt=2500).count()

            Z = ztest(top_p, low_p, top_pop, low_pop)
            if math.fabs(Z) > 1.96:
                j[c.name] = (top_p, low_p, top_pop, low_pop, Z)
        dd[str(pull_date)] = j

    rval = {'data': dd}
    #print data_3v3.objects.all().count()
    #dd = data_3v3.objects.filter(**klob).values_list('ranking', flat=True)
    #j = {"count": len(dd), "average": 1.0*sum(dd)/len(dd), "lowest": max(dd), "highest": min(dd)}
    return JsonResponse(rval)
