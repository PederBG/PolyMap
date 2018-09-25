from django.core.management.base import BaseCommand
from polygons.models import Polygon
import json
from geojson import FeatureCollection, dump

# Looping through polygon objects in database to generate geojson file
class Command(BaseCommand):

    def handle(self, *args, **options):
        print('saving...')
        feature_collection = FeatureCollection( [poly.getJson() for poly in Polygon.objects.all()] )

        with open('/tmp/polygons.geojson', 'w+') as f:
            dump(feature_collection, f)
        print('saved')
