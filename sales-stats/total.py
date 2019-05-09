import csv
import matplotlib.pyplot as plt
import numpy as np

ms = {'Jan':0,'Feb':1,'Mar':2,'Apr':3,'May':4,'Jun':5,'Jul':6,'Aug':7,'Sep':8,
      'Oct':9,'Nov':10,'Dec':11}

yrs = {}
yrs2 = {}
for y in range(2011,2019):
    yrs[str(y)] = [0]*12
    yrs2[str(y)] = 0
    
with open('ev_sales.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[0] not in yrs:
            continue
        yrs[row[0]][ms[row[1][:3]]] = float(row[4])
        yrs2[row[0]] += float(row[4])

av = [0]*12
for y in yrs:
    for m in range(12):
        av[m] += yrs[y][m]/8

b = []
for y in yrs:
    b += [yrs2[y]]
    for m in range(12):
        yrs[y][m] = yrs[y][m]/av[m]

plt.figure()
plt.plot([1]*12,c='k',ls=':')
#plt.plot(av,c='k',ls=':')
plt.plot(yrs['2018'])
plt.plot(yrs['2017'])
plt.plot(yrs['2016'])

plt.figure()
plt.bar(range(2011,2019),b)
plt.title('UK New Vehicle Registrations')
plt.show()
