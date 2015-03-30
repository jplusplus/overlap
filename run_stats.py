#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Create weighed data by running some statistics though the the output
   of `create_factors.py`.

   The input should have an id column with id's corresponding to `id_2`
   in `create_factors.py`. The output will be a CSV with two columns,
   where the first, `id`, corresponds to `id_1` in `create_factors.py`.

   run_stats --id province --value num_camels
             --factors factors.json --input input.csv

   factors.json:
     "Värmlands län": {"Värmland": 1, "Dalarna": .03},
     "Dalarnas län": {"Dalarna": .97}

   input.csv:
     province, num_camels
     Värmland, 12
     Dalarna, 20

   output.csv:
     Värmlands län, 13
     Dalarnas län. 19
"""

from json import load as load_json
from datasheet import CSVFile
from csv import writer as csvWriter

factor_filename = "factors.json"
input_filename = "../2014_riksdagsval.csv"
output_filename = "output.csv"
id_column = "vd"
value_column = "V|S|MP|C|FP|KD|M|SD|FI"

value_columns = value_column.split("|")

data = CSVFile(input_filename)

with open(factor_filename) as file_:
    factors = load_json(file_)

output = []
for id_, dict_ in factors.iteritems():
    sum_ = {}
    for column in value_columns:
        sum_[column] = 0

    for id_2, val in dict_.iteritems():
        for data_row in data.get_next():
            if data_row[id_column] == id_2:
                for column in value_columns:
                    sum_[column] += val * float(data_row[column])
    row = [id_]
    for column in value_columns:
        row.append(sum_[column])
    output.append(row)

with open(output_filename, 'wb') as csvfile:
    csv_writer = csvWriter(csvfile, delimiter=',', quotechar='"')
    csv_writer.writerow([id_column] + value_columns)
    for row in output:
        csv_writer.writerow(row)
