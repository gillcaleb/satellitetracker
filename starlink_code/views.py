from django.shortcuts import render
from satellite_tracker import settings
from starlink_code import functions
from django.http import HttpResponse
import os
from .forms import configForm
# Create your views here.

def get_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = configForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            print("FORM VALIDATED")
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

        else:
            print(form.errors)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = configForm()

    return render(request, 'test.html', {'form': form})

def hello_world(request):
    direc = settings.MEDIA_ROOT
    return render(request, 'index.html', {'directory':direc})

def test_feature(request):
    #functions.referenceDB(settings.UPDATE_URL)
    return render(request, 'test.html')

def download_file(request):
    #functions.populateDB('https://celestrak.com/NORAD/elements/gp.php?GROUP=starlink&FORMAT=TLE')
    #functions.networkLink("networklink.kml","http://localhost:8000/downloadupdate")
    functions.initializeFile()

    file_path = os.path.join(settings.MEDIA_ROOT, "networkLink.kml")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.google-earth.kml+xml")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def download_update(request):
    functions.initializeFile()
    file_path = os.path.join(settings.MEDIA_ROOT, "starlink.kml")
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
