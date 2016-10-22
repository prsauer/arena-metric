from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def db(request):

    return render(request, 'db.html', {})

def pepe(request):
    r = {"response_type": "in_channel"}
    im = "http://i3.kym-cdn.com/photos/images/facebook/000/862/065/0e9.jpg"
    attachments = [{"image": im},]
    r['attachments'] = attachments
    return JsonResponse(r)
