from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Pepe

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def db(request):

    return render(request, 'db.html', {})

def pepe(request):
    if request.GET.get('text') and request.GET.get('text') == 'help':
        tm = "<table><thead><td>Command</td><td>Pepe</td></thead><tbody>"
        for p in Pepe.objects.all():
            tr = "<tr><td>%s</td><td><img src=\"%s\"></img></td></tr>"%(p.command, p.url)
            tm+=tr
        tm+="</tbody></table>"
        return HttpResponse(tm)
    try:
        r = {"response_type": "in_channel"}
        im = Pepe.objects.get(command=request.GET.get('text')).url
        attachments = [{"image_url": im},]
        r['attachments'] = attachments
        return JsonResponse(r)
    except:
        r = {"response_type": "in_channel"}
        im = "http://i3.kym-cdn.com/photos/images/facebook/000/862/065/0e9.jpg"
        attachments = [{"image_url": im},]
        r['attachments'] = attachments
        return JsonResponse(r)
