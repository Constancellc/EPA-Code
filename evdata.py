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
5 - driven wheels
6 - weight
7 - axle ratio
8 - n/v ratio
9 - cycle
10 - fe
11:13 - target coefficients

"""

import csv
c=1

# THESE ARE NOT VALID FILES TO PREVENT ACCIDENTAL DAMAGE
cycle = 'Charge Depleting Highway'
out = 'ev_data.csv'

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
#ids = []

for year in data:
    new = []
    with open(year, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # pick out the same drive cycles
            if row[36] == 'Electricity':
                
                if row[34] == 'Charge Depleting Highway':
                    row[34] = '1'
                elif row[34] == 'Charge Depleting UDDS':
                    row[34] = '2'
                else:
                    row[34] = '0'
                    
                if row[45] == '0' or row[45] == '':
                    continue
                else:
                    c = c+1
                    print c
                    new.append(row),
    newlist = []

    for row in new:
        if row[17] == 'F' or row[17] == 'R':
            row[17] = 2
        else:
            row[17] = 4
            
        if year in older:
            store = [row[0],row[3]+" "+row[4],row[7],row[10],row[17],row[21],\
                     row[22],row[23],row[34],row[45],row[51],row[52],row[53]]
        else:
            store = [row[0],row[3]+" "+row[4],row[7],row[10],row[17],row[21],\
                     row[22],row[23],row[34],row[45],row[54],row[55],row[56]]
        newlist.append(store),
        
    for row in newlist:
        save.append(row),

# Write the reduced data to a csv file
with open(out, 'wb') as h:
    writer = csv.writer(h)
    writer.writerows(save)
