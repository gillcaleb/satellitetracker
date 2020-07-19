from django.core.management.base import BaseCommand
from satellite_tracker import settings
from starlink_code import functions
from starlink_code.models import satelliteTLE
import requests

class Command(BaseCommand):
    help = 'Populates database with celestrak data'

    def handle(self,*args, **kwargs):
        #clear existing contents of satelliteTLE
        try:
            satelliteTLE.objects.all().delete()
        except:
            print("Error in deleting DB contents")

        #fetch data from celestrak and clean to usable format
        tle = functions.fetchTLES(settings.UPDATE_URL)

        #add cleaned data to the satelliteTLE model
        try:
            for i in tle:

                s = satelliteTLE(name=i[0].decode("utf-8"), L1=i[1].decode("utf-8"), L2=i[2].decode("utf-8"))
                s.save()
            print(satelliteTLE.objects.all().count())
        except:
            print("Error adding data to DB")
        return
