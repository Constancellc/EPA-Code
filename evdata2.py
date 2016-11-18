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
9:11 - target coefficients
12 - highways fe
13 - udds fe
"""

import csv
# arbitrary counter so there is somethng to watch on terminal
c=1

# where we're writing to
out = 'pureEVdata.csv'

data = ['EPA/10tstcar.csv','EPA/11tstcar.csv','EPA/12tstcar.csv',\
        'EPA/13tstcar.csv','EPA/14tstcar.csv','EPA/15tstcar.csv',\
        'EPA/16tstcar.csv','EPA/17tstcar.csv']

# Older years have slightly different headings :(
older = ['EPA/10tstcar.csv','EPA/11tstcar.csv','EPA/12tstcar.csv',\
        'EPA/13tstcar.csv']

save = []
ids = []

highways = {}
udds = {}
parameters = {}
targets = {}

for year in data:
    new = []
    with open(year, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # pick out the same drive cycles
            if row[36] == 'Electricity':

                # changes driven wheels info to numbers (for matlab)
                if row[17] == 'F' or row[17] == 'R':
                    row[17] = 2
                else:
                    row[17] = 4

                # Let's chuck out the vehicles which have engines (hybrids)
                engineSize = float(row[7])
                if engineSize >= 0.2 and engineSize <= 10:
                    continue
                else:
                    if row[45] == '0' or row[45] == '':
                        continue
                    else:
                        # Add the fuel efficiency to the relevant drive cycle
                        # dictionary using the vehicle ID as a key
                        if row[34] == 'Charge Depleting Highway':
                            fe = float(row[45])
                            if fe <= 40:
                                fe = 3700/fe
                            highways[row[5]] = str(fe)
                        elif row[34] == 'Charge Depleting UDDS':
                            fe = float(row[45])
                            if fe <= 40:
                                fe = 3700/fe
                            udds[row[5]] = str(fe)

                        # now get the chosen vehicle parameters    
                        parameters[row[5]] = [row[0],row[3]+" "+row[4],row[7],\
                                              row[10],row[17],row[21],row[22],\
                                              row[23]]
                        # and finally the target coefficients
                        if year in older:
                            targets[row[5]] = [row[51],row[52],row[53]]
                        else:
                            targets[row[5]] = [row[54],row[55],row[56]]

                        # Lastly store the vehicle ID
                        if row[5] in ids:
                            continue
                        else:
                            ids.append(row[5])
                            
                        c = c+1
                        print c

newlist = []

for id in ids:
    flag = 0
    
    try:
        highways[id]
    except KeyError:
        flag = 1
    try:
        udds[id]
    except KeyError:
        flag = 1

    if flag == 0:
        store = parameters[id]+targets[id]+[highways[id],udds[id]]
        newlist.append(store)

# Write the reduced data to a csv file
with open(out, 'wb') as h:
    writer = csv.writer(h)
    writer.writerows(newlist)
