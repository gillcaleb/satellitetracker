from django.shortcuts import render
from satellite_tracker import settings
from django.http import HttpResponse
import os

# Create your views here.
def hello_world(request):
    return render(request, 'index.html', {})

def download_file(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'starlink.kml')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.google-earth.kml+xml")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
