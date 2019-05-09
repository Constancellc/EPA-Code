import csv
import matplotlib.pyplot as plt
import numpy as np
import random

total = {}
_2017 = {}
_2018 = {}
name = {}

with open('veh0105.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    next(reader)
    for row in reader:
        if row[0] == '':
            continue
        if row[0][0] not in ['E','S','W']:
            continue
        total[row[0]] = float(row[2].replace(',',''))*1000
        name[row[0]] = row[1]
        if name[row[0]][-3:] == ' UA':
            name[row[0]] = name[row[0]][:-3]

with open('EVregionalSales.csv','r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] == '':
            continue
        if row[0][:2] not in ['E0','S0','W0']:
            continue
        try:
            _2018[row[0]] = (float(row[2])+float(row[3])+float(row[4]))/\
                            (0.806*total[row[0]])
            _2017[row[0]] = (float(row[5])+float(row[6])+float(row[7])+\
                             float(row[8]))/total[row[0]]
        except:
            continue


clrs = ['#ff0000','#ff4000','#ff8000','#ffbf00','#bfff00','#80ff00','#40ff00',
        '#00ff00','#00ff40','#00ff80','#00ffbf','#00ffff','#00bfff','#0080ff',
        '#0040ff','#0000ff','#4000ff','#8000ff','#bf00ff','#ff00ff','#ff00bf',
        '#ff0080','#ff0040','#ff0000']


plt.figure(figsize=(18,12))
plt.rcParams['font.size'] = 14
for c in _2018:
    
    i = int(random.random()*len(clrs))
    plt.scatter([np.log(_2018[c]*100)],[100*(_2018[c]-_2017[c])/_2017[c]],
                total[c]/1000,clrs[i],alpha=0.5)
    if _2018[c] > 0.04 or _2018[c] > 1.6*_2017[c] or \
       c in ['E07000179','S12000040','E07000178']:
        plt.annotate(name[c],(np.log(_2018[c]*100),
                              100*(_2018[c]-_2017[c])/_2017[c]),
                     color=clrs[i])
plt.xticks([np.log(0.5),np.log(1),np.log(2),np.log(5),np.log(10),np.log(20),
            np.log(50),np.log(100)],
           ['0.5','1','2','5','10','20','50','100'])
plt.ylabel('% Change from Last Year')
plt.xlabel('% New Sales Electric (2018)')
plt.grid()
plt.tight_layout()
plt.show()
        
