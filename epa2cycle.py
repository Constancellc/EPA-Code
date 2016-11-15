"""
THIS FUNCTION TAKES THE RAW EPA DATA AND PICKS OUT A SPECIFIC DRIVECYCLE,
STORING ONLY ONE TEST PER VEHICLE.

THE RESULTS ARE ADDED TO THE CSV FILE 'OUT'

RUN THIS SCRIPT WITH CAUTION TO AVOID CREATING DUPLICATES!!!

THE OUTPUT CSV FILE CONTAINS THE FOLLOWING FIELDS:

1 - year
2 - brand + model
3 - engine size (l)
4 - horsepower
5 - cylinders
6 - gears
7 - drive
8 - weight
9 - axle ratio
10 - n/v ratio
11 - fuel
12 - C02
13 - fe
14:16 - target coefficients

"""

import csv
c=1

# THESE ARE NOT VALID FILES TO PREVENT ACCIDENTAL DAMAGE
cycle = 'Charge Depleting Highway'
out = 'cd_highway.csv'

data = ['EPA/10tstcar.csv','EPA/11tstcar.csv','EPA/12tstcar.csv',\
        'EPA/13tstcar.csv','EPA/14tstcar.csv','EPA/15tstcar.csv',\
        'EPA/16tstcar.csv','EPA/17tstcar.csv']

# Older years have slightly different headings :(
older = ['EPA/10tstcar.csv','EPA/11tstcar.csv','EPA/12tstcar.csv',\
        'EPA/13tstcar.csv']
"""
# Let's avoid writing over what we already have
with open(out) as s:
    save = list(csv.reader(s))
"""
save = []
ids = []

for year in data:
    new = []
    with open(year, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # pick out the same drive cycles
            if row[34] == cycle:
                c = c+1
                print c
                new.append(row),
    newlist = []

    # store only the first test of each vehicle
    for row in new:
        if row[5] in ids:
            continue
        else:
            ids.append(row[5])
            if year in older:
                store = [row[0],row[3]+" "+row[4],row[7],row[10],row[11],row[15],\
                         row[17],row[21],row[22],row[23],row[36],row[40],row[45],\
                         row[51],row[52],row[53]]
            else:
                store = [row[0],row[3]+" "+row[4],row[7],row[10],row[11],row[15],\
                         row[17],row[21],row[22],row[23],row[36],row[40],row[45],\
                         row[54],row[55],row[56]]
            newlist.append(store),
        
    for row in newlist:
        save.append(row),

# Write the reduced data to a csv file
with open(out, 'wb') as h:
    writer = csv.writer(h)
    writer.writerows(save)
