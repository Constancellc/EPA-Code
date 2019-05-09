import csv
import matplotlib.pyplot as plt
import numpy as np


pureEVs = {}

with open('ev_sales.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if float(row[0]) not in pureEVs:
            pureEVs[float(row[0])] = float(row[2])
        else:
            pureEVs[float(row[0])] += float(row[2])

t = range(2011,2019)
y = [0.0]
for i in range(len(t)):
    y.append((y[i]*1000+pureEVs[t[i]])/1000)

plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.bar(t,y[1:],zorder=2)
plt.ylabel('Thousands of Vehicles')
plt.xlabel('Year')
plt.grid(zorder=0.5)
plt.show()
    
