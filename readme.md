The problem
-----------
You have two different, overlapping administrative divisions, and want statistics based on one of the extrapolated to the other.

Case: We have hardly any demographic data for the 15,000 or so Swedish postal codes. On the other hand we have plenty of interesting data on the ≈ 6,000 electorial districts. Given a fairly large dataset where we know the postal codes, we can extrapolate statistics from electorial districts, and get a fair approximation.

The solution
------------
Use your favourite GIS software to intersect the two administrative systems. Create a .dfb (QGIS) or .csv file containing an area column for the intersection. Run the file through `create_factors.py`, to create a table of weighing factors. Then run your statistics through `run_stats.py` to apply.

This will obviously only create useful results for fairly small and homogenous administrative entities, and fairly large datasets. Common sense is your friend here.

Example
-------
We have two administrative systems: Counties and provinces. We know the number of camels in each province:

     province, num_camels
     Värmland, 12
     Dalarna, 20

Now we want to know the approximate number of camels in each county.

1. Using QGIS, we produce a .dbf file with all intersections:

     `ID  county           province    area`
     `1   Värmlands län    Värmland    190`
     `2   Värmlands län    Dalarna     6`
     `3   Dalarnas län     Dalarna     180`

2. Then we run `weighted_data --id_1 county --id_2 province --area area` to produce a json file, `factors.json`, with weighing factors:

     `"Värmlands län": {"Värmland": 1, "Dalarna": .03},`
     `"Dalarnas län": {"Dalarna": .97}`

3. Finally, we run our camel data through this filter, `run_stats --id province --value num_camels --factors factors.json --input input.csv`  greger

    `Värmlands län, 13`
    `Dalarnas län, 19`

