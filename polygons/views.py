from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.core.management import call_command
from .models import Polygon

import shapely.geometry as geom
from shapely.ops import cascaded_union
import geojson
import json
from itertools import combinations


def index(request):
    return render(request, 'polygons/index.html',{
        "polygons": Polygon.objects.all(),
    })


# Tips: geojson files are easy to make at http://geojson.io
def upload(request):
    # Validating input file
    try:
        infile = request.FILES['file'].read().decode('utf8').replace("'", '"')
        jsondata = json.loads(infile)
    except (MultiValueDictKeyError, ValueError):
        return JsonResponse({'code': 400, 'text': 'Error: Not a valid json file'})

    Polygon.objects.all().delete()
    for feature in jsondata['features']:
        p = Polygon()
        p.grids = str(feature)
        p.save()

    return JsonResponse({'code': 200, 'text': 'Success!'})


def save(request):
    call_command('save_geojson')
    with open('/tmp/polygons.geojson', 'r') as f:
        response = HttpResponse(f, content_type="application/vnd.geo+json")
        response['Content-Disposition'] = 'attachment; filename=polygons.geojson'
        return response


def union(request, ids):
    return runOperation(ids, request.resolver_match.url_name)


def intersect(request, ids):
    return runOperation(ids, request.resolver_match.url_name)



# Function for doing the union and intersect operations
def runOperation(ids, operation):
    input_polygons = [ Polygon.objects.filter(id=tmp).first() for tmp in ids.split(',') ]

    # Removing input polygons from db
    removePolys(input_polygons)

    # Translate into shapely object
    polygons = shapelify(input_polygons)

    if operation == 'intersect':
        # Recursivly finds intersections, also handles concave polygons
        multipolygon = recursiveIntersect(polygons, 0, polygons[0])
        if multipolygon.is_empty:
            return JsonResponse({'code': 200, 'text': 'Success'})

    elif operation == 'union':
        # Taking union using shapely package
        multipolygon = cascaded_union(polygons)

    else:
        return JsonResponse({'code': 400, 'text': 'Bad request'})

    # Spliting into polygons if output is a multipolygon
    new_polygons = splitMulti(multipolygon)

    # Convert back from WKT to geojson and add new polygon(s) to db
    for poly in new_polygons:
        addPolys(geojson.Feature(geometry=poly, properties={}))

    return JsonResponse({'code': 200, 'text': 'Success'})


# Help functions

def removePolys(input_polygons):
    for elem in input_polygons:
        Polygon.objects.filter(id=elem.id).delete()

def addPolys(geojson_out):
    p = Polygon()
    p.grids = str(geojson_out)
    p.save()

def shapelify(in_polys):
    polygons = []
    for poly in in_polys:
        polygons.append(geom.asShape(poly.getJson()['geometry']))
    return polygons

def splitMulti(multi):
    if multi.geom_type == 'MultiPolygon':
        return list(multi)
    else:
        return [multi]

def recursiveIntersect(multi, i, current):
    if i == len(multi):
        return current
    partial_intersect = splitMulti( current.intersection(multi[i]) )
    fragment_list = [recursiveIntersect(multi, i+1, fragment) for fragment in partial_intersect]
    return cascaded_union(fragment_list)
