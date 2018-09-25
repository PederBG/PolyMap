from django.db import models
import ast, json

class Polygon(models.Model):
    grids = models.TextField(max_length=5000)

    def getJson(self):
        formated = json.dumps(ast.literal_eval(self.grids))
        return json.loads(formated)

    def getGrids(self):
        return self.getJson()['geometry']['coordinates'][0]
