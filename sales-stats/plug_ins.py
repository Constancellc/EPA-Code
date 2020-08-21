import csv
import matplotlib.pyplot as plt
import numpy as np


pureEVs = {}

with open('ev_sales.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if float(row[0]) not in pureEVs:
            pureEVs[float(row[0])] = float(row[3])
        else:
            pureEVs[float(row[0])] += float(row[3])

print(pureEVs)
t = range(2011,2021)
y = [0.0]
for i in range(len(t)):
    y.append((y[-1]*1000+pureEVs[t[i]])/1000)

print(y[-1])
plt.figure(figsize=(6,2.5))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 11
plt.bar(t,y[1:],zorder=2)
plt.ylabel('Thousands of Vehicles')
plt.xlabel('Year')
plt.grid(zorder=0.5)
plt.xticks(range(2011,2021),['2011','2012','2013','2014','2015','2016',
                             '2017','2018','2019','202'])
plt.tight_layout()
plt.savefig('../../Dropbox/thesis/chapter1/sales.eps', format='eps',
            dpi=300, bbox_inches='tight', pad_inches=0.0)
plt.show()
    
