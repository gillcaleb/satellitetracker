import ephem
from datetime import datetime, timedelta
import simplekml
import requests
import time
import os
from satellite_tracker import settings
#from starlink_code.models import satelliteTLE

satellite_array = []

#Fetch data from celestrak
def fetchTLES(URL):
    global satellite_array
    raw = []
    try:
        req = requests.get(URL)
        text = req.text
        newtext = text.encode("ascii","ignore")
        raw = newtext.splitlines()
        satellite_array = [raw[i:i+3] for i in range(0, len(raw), 3)]
        return satellite_array
    except:
        print("Data could not be returned from Celestrak - check if URL is correct and serving properly")
        return

#End database functions========================================================

def generateKMLConstellation(filename):
    global satellite_array
    kml = simplekml.Kml()
    time = datetime.now()
    for tle in satellite_array:
        sat = ephem.readtle(tle[0].decode("utf-8"),tle[1].decode("utf-8"),tle[2].decode("utf-8"))
        sat.compute(time)
        currentSat = kml.newpoint(name=tle[0].decode("utf-8"))
        currentSat.coords = [(sat.sublong, sat.sublat, sat.elevation)]
        currentSat.altitudemode = simplekml.AltitudeMode.relativetoground
        currentSat.extrude = 1
        currentSat.style.labelstyle.scale = 1.5
        currentSat.style.iconstyle.icon.href = 'downloadicon'

    filename =  os.path.join(settings.MEDIA_ROOT, filename)
    kml.save(filename)
    return

def networkLink(name,refresh):

    fetchTLES(settings.UPDATE_URL)

    kml = simplekml.Kml()
    netlink = kml.newnetworklink(name="Network Link")
    netlink.link.href =  settings.STATIC_IP + '/downloadupdate'
    netlink.link.refreshinterval = refresh
    netlink.link.refreshmode = simplekml.RefreshMode.oninterval
    filename =  os.path.join(settings.MEDIA_ROOT, name)
    kml.save(filename)
    return

def updateStarLink():
    file_path = os.path.join(settings.MEDIA_ROOT, 'starlink.kml')
    if os.path.exists(file_path):
        os.remove(file_path)
    generateKMLConstellation('starlink.kml')
