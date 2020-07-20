import ephem
from datetime import datetime, timedelta
import simplekml
import requests
import time
import os
from satellite_tracker import settings
from starlink_code.models import satelliteTLE

#Database functions============================================================

#Update database - this will run priodically
def updateDB():

    #implement file hash comparison or last update check here


    #Fetch data from Celestrak
    sats = fetchTLES(settings.UPDATE_URL)

    #Iterate over list of satellites
    for sat in sats:

        #Query based on name
        q1 = satelliteTLE.objects.filter(name=sat[0].decode("utf-8"))

        #if satellite is NOT present, add it to the table
        if not q1:
            print('Satellite not found')
            s = satelliteTLE(name=sat[0].decode("utf-8"), L1=sat[1].decode("utf-8"), L2=sat[2].decode("utf-8"))
            s.save()
        #if satellite is present, update the TLE L1 and L2
        else:
            q1.update(L1=sat[1].decode("utf-8"), L2=sat[2].decode("utf-8"))

    return

#Fetch data from celestrak
def fetchTLES(URL):
    raw = []
    tle = []
    try:
        req = requests.get(URL)
        text = req.text
        newtext = text.encode("ascii","ignore")
        raw = newtext.splitlines()
        tle = [raw[i:i+3] for i in range(0, len(raw), 3)]
        return tle
    except:
        print("Data could not be returned from Celestrak - check if URL is correct and serving properly")
        return

#End database functions========================================================



#TODO: raise line to satellite elevation, fix issue of incorrect lines
def generateLineString(tleList,kmlfile,timeoffset):

    for tle in tleList:
        sat = ephem.readtle(tle[0].decode("utf-8"),tle[1].decode("utf-8"), tle[2].decode("utf-8"))
        sat.compute(datetime.now() - timedelta(minutes=timeoffset))
        past = (sat.sublong, sat.sublat, sat.elevation)
        sat.compute(datetime.now() + timedelta(minutes=timeoffset))
        future = (sat.sublong, sat.sublat,sat.elevation)
        currentline = kmlfile.newlinestring(gxaltitudeoffset=int(sat.elevation))
        currentline.coords = [past, future]
        currentline.altitudemode = simplekml.AltitudeMode.clamptoground

def generateKMLObserver(kml, latitude, longitude):
    time = datetime.now()
    station = setObserver(latitude,longitude,time)
    for tle in satelliteTLE.objects.all():
        sat = ephem.readtle(tle.name, tle.L1, tle.L2)
        sat.compute(station)
        if sat.alt > ephem.degrees('9.0'):
            sat.compute(time)
            currentSat = kml.newpoint(name=tle.name)
            currentSat.coords = [(sat.sublong, sat.sublat, sat.elevation)]
            currentSat.altitudemode = simplekml.AltitudeMode.relativetoground
            currentSat.extrude = 1
            currentSat.style.labelstyle.scale = 1.5
            currentSat.style.iconstyle.icon.href = 'downloadicon'
    #generateLineString(tleList,kml,5)

    filename =  os.path.join(settings.MEDIA_ROOT, 'starlink.kml')
    kml.save(filename)
    return

def generateKMLConstellation(kml):
    time = datetime.now()
    for tle in satelliteTLE.objects.all():
        sat = ephem.readtle(tle.name, tle.L1, tle.L2)
        sat.compute(time)
        currentSat = kml.newpoint(name=tle.name)
        currentSat.coords = [(sat.sublong, sat.sublat, sat.elevation)]
        currentSat.altitudemode = simplekml.AltitudeMode.relativetoground
        currentSat.extrude = 1
        currentSat.style.labelstyle.scale = 1.5
        currentSat.style.iconstyle.icon.href = 'downloadicon'
    #generateLineString(tleList,kml,5)

    filename =  os.path.join(settings.MEDIA_ROOT, 'starlink.kml')
    kml.save(filename)
    return


def setObserver(lat,lon,time):
    station = ephem.Observer()
    station.lat = lat
    station.lon = lon
    station.date = time
    return station

def networkLink(name,refresh):
    kml = simplekml.Kml()
    netlink = kml.newnetworklink(name="Network Link")
    netlink.link.href = 'http://'+ settings.STATIC_IP + ':8000/downloadupdate'
    netlink.link.refreshinterval = refresh
    netlink.link.refreshmode = simplekml.RefreshMode.oninterval
    filename =  os.path.join(settings.MEDIA_ROOT, name)
    kml.save(filename)
    return


def initializeFile():
    file_path = os.path.join(settings.MEDIA_ROOT, "starlink.kml")
    if os.path.exists(file_path):
        os.remove(file_path)
    kml = simplekml.Kml()
    generateKMLConstellation(kml)
