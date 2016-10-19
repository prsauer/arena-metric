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

def dates(request):
    set_of_dates = set()
    k = data_3v3.objects.filter(classId=1,
       raceId=1).order_by('pull_date').values_list('pull_date', flat=True)
    for date in k:
        print date
        set_of_dates.add(date)
    d = list()

    set_of_dates = [x for x in set_of_dates]
    set_of_dates.sort()
    set_of_dates.reverse()

    for date in set_of_dates:
        d.append(date.strftime("%Y-%m-%d-%H-%M"))

    return JsonResponse(d, safe=False)

# Create your views here.
def main(request):
    klob = {}
    for k in request.GET.keys():
        if k == 'pull_date':
            parts = request.GET.get(k).split('-')
            klob['pull_date__year']=parts[0]
            klob['pull_date__month']=parts[1]
            klob['pull_date__day']=parts[2]
            klob['pull_date__hour']=parts[3]
            klob['pull_date__minute']=parts[4]
        else:
            klob[k] = request.GET.get(k)
    #print k
    if 'pull_date__year' in klob.keys():
        dd = data_3v3.objects.filter(**klob).order_by('ranking')[0:25]
    else:
        dd = data_3v3.fresh.filter(**klob).order_by('ranking')[0:25]
    #print dd.last().__dict__
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
