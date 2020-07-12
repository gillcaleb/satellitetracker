import ephem
from datetime import datetime, timedelta
import simplekml
import requests
import time
import os
from satellite_tracker import settings
from starlink_code.models import satelliteTLE

def populateDB(url):
    raw = []
    tle = []
    try:
        req = requests.get(url)
        text = req.text
        newtext = text.encode("ascii","ignore")
        raw = newtext.splitlines()
        tle = [raw[i:i+3] for i in range(0, len(raw), 3)]
    except:
        print("Data could not be returned - check if URL is correct and serving properly")

    try:
        for i in tle:
            s = satelliteTLE(name=i[0].decode("utf-8"), L1=i[0].decode("utf-8"), L2=i[2].decode("utf-8"))
            s.save()
        print(satelliteTLE.objects.all())
    except:
        print("error adding to DB")
    return

def getTLE(url):
    raw = []
    tle = []
    try:
        req = requests.get(url)
        text = req.text
        newtext = text.encode("ascii","ignore")
        raw = newtext.splitlines()
        tle = [raw[i:i+3] for i in range(0, len(raw), 3)]
    except:
        print("Data could not be returned - check if URL is correct and serving properly")
    return tle

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


def generateKML(kml, tleList):
    time = datetime.now()
    station = setObserver('42.3601','-71.0589',time)
    for tle in tleList:
        sat = ephem.readtle(tle[0].decode("utf-8"),tle[1].decode("utf-8"), tle[2].decode("utf-8"))
        sat.compute(station)
        if sat.alt > ephem.degrees('9.0'):
            sat.compute(time)
            currentSat = kml.newpoint(name=tle[0].decode("utf-8"))
            currentSat.coords = [(sat.sublong, sat.sublat, sat.elevation)]
            currentSat.altitudemode = simplekml.AltitudeMode.relativetoground
            currentSat.extrude = 1
            currentSat.style.labelstyle.scale = 1.5
            currentSat.style.iconstyle.icon.href = 'http://localhost:8000/downloadicon'
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

def networkLink(name,URL):
    kml = simplekml.Kml()
    netlink = kml.newnetworklink(name="Network Link")
    netlink.link.href = URL
    netlink.link.refreshinterval = 10
    netlink.link.refreshmode = simplekml.RefreshMode.oninterval
    filename = filename =  os.path.join(settings.MEDIA_ROOT, name)
    kml.save(filename)
    return


def initializeFile(TLE_URL):
    tleList = getTLE(TLE_URL)
    file_path = os.path.join(settings.MEDIA_ROOT, "starlink.kml")
    if os.path.exists(file_path):
        os.remove(file_path)
    kml = simplekml.Kml()
    generateKML(kml, tleList)

"""
if __name__ in "__main__":

    tleList = getTLE("https://celestrak.com/NORAD/elements/gp.php?GROUP=starlink&FORMAT=TLE")

    networkLink( "http://localhost:8001/starlink.kml")
    kml = simplekml.Kml()
    generateKML(kml, tleList)

    while True:
        open("starlink.kml", 'w').close()
        kml = simplekml.Kml()
        generateKML(kml, tleList)
        time.sleep(8)
"""
