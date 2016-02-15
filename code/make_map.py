from lingpy import *
import pickle
import geojson
import json

L = pickle.load(open('../bin/languages.bin', 'rb'))

languages = csv2list('../tsv/doculects.tsv')

points = []
for line in languages[1:]:
    lang = line[3]
    if line[0].startswith('*'):
        color = '#00ff00'
    else:
        color = '#ff0000'
    try:
        lat, lon = L[lang]['coordinates']['latitude'], L[lang]['coordinates']['longitude']
        point = geojson.Point((lon, lat))
        feature = geojson.Feature(geometry=point,
                properties={
                    "doculect" : line[0],
                    "glottolog" : lang,
                    "group" : line[5],
                    "source" : line[6],
                    "entries" : line[7],
                    "marker-color" : color
                    }
                )
        points += [feature]
    except: 
        print("No luck with {0}...".format(lang))

with open('../json/languages.geojson', 'w') as f:
    f.write(json.dumps(geojson.FeatureCollection(points)))

