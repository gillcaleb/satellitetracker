from django.shortcuts import render
from satellite_tracker import settings
from starlink_code import functions
from django.http import HttpResponse
import os

# Create your views here.
def hello_world(request):
    direc = settings.MEDIA_ROOT
    return render(request, 'index.html', {'directory':direc})

def download_file(request):
    functions.initializeFile('https://celestrak.com/NORAD/elements/gp.php?GROUP=starlink&FORMAT=TLE', "networklink.kml")

    file_path = os.path.join(settings.MEDIA_ROOT, 'starlink.kml')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.google-earth.kml+xml")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def download_icon(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'satelliteimage.png')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="image/png")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
