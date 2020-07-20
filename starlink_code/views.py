from django.shortcuts import render
from satellite_tracker import settings
from starlink_code import functions
from django.http import HttpResponse
import os
from .forms import configForm

def test(request):
    functions.updateDB()
    return render(request, 'index.html')

def index(request):
    if request.method == 'POST':
        # if button is pressed, return default 10sec refresh with link to the starlink file
        functions.networkLink("networklink.kml",10)
        functions.initializeFile()

        file_path = os.path.join(settings.MEDIA_ROOT, "networkLink.kml")
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.google-earth.kml+xml")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
    return render(request, 'index.html')

def get_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = configForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            if form.data['view'] == "on":
                functions.networkLink(form.data['filename'], form.data['refresh'])
                functions.initializeFile()

                file_path = os.path.join(settings.MEDIA_ROOT, form.data['filename'])
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as fh:
                        response = HttpResponse(fh.read(), content_type="application/vnd.google-earth.kml+xml")
                        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                        return response
                raise Http404

            else:
                return render(request, 'submitted.html')

        else:
            print(form.errors)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = configForm()

    return render(request, 'form.html', {'form': form})

def download_file(request):
    functions.networkLink("networklink.kml",10)
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
