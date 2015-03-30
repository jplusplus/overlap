#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Given a DBF file, two overlapping ID columns, and an area column,
   this script will return a json with weighing factors for each ID1.

   The DBF file is typically produced by intersecting two vector layers
   in QGIS.

   e.g.:

     ID  county           province    area
     1   Värmlands län    Värmland    190
     2   Värmlands län    Dalarna     6
     3   Dalarnas län     Dalarna     180

   weighted_data --id_1 county --id_2 province --area area

     "Värmlands län": {"Värmland": 1, "Dalarna": .03},
     "Dalarnas län": {"Dalarna": .97}
"""

from datasheet import DBFFile, CSVFile
from magic import from_file as magic_from_file
from json import dump as json_dump

filename = "intersect.dbf"
id_1_column = "POSTALCODE"
id_2_column = "VD"
area_column = "AREA"
output = "factors.json"
min_area = 0

file_mime_type = magic_from_file(filename, mime=True)
if file_mime_type == "text/plain":
    dataset = CSVFile(filename)
elif file_mime_type == "application/x-dbf":
    dataset = DBFFile(filename)
else:
    print("Unknown mime type: %s" % file_mime_type)

every_id_1 = set()
id_2_sums = {}
id_map = {}

for row in dataset.get_next():
    if (area_column in row.keys()) and \
       (row[area_column] > min_area):
        id_1 = row[id_1_column]
        id_2 = row[id_2_column]
        area = row[area_column]

        every_id_1.add(id_1)

        if id_1 not in id_map:
            id_map[id_1] = {}

        if id_2 not in id_map[id_1]:
            id_map[id_1][id_2] = float(area)
        else:
            print "Duplicate intersections for %s and %s!" % (id_1, id_2)

        if id_2 in id_2_sums:
            id_2_sums[id_2] += float(area)
        else:
            id_2_sums[id_2] = float(area)

result = {}
for id_1, id_2s in id_map.iteritems():
    if id_1 not in result:
        result[id_1] = {}
    for id_2, area in id_2s.iteritems():
        sum = id_2_sums[id_2]
        result[id_1][id_2] = float(area) / float(sum)

with open(output, 'wb') as outfile:
    json_dump(result, outfile, encoding='utf-8')
