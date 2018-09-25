from django.core.management.base import BaseCommand
from polygons.models import Polygon
import json


# Help funtion, not used
class Command(BaseCommand):
    args = '<foo bar ..>'
    help = "No options needed"

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        if len(args) != 1:
            print("Command only supports one argument")
        else:
            with open(args[0], 'r') as data_file:
                Polygon.objects.all().delete()
                data = json.load(data_file)
                for feature in data['features']:
                    p = Polygon()
                    p.grids = str(feature)
                    p.save()
